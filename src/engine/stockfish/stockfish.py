from typing import Optional, Union
from os import cpu_count
from queue import SimpleQueue
from asyncio import TaskGroup, sleep
from time import perf_counter

from .worker import StockfishWorker


class LocalStockfishEngine:
    """
    Local Stockfish Engine

    Args:
        path (str): Path to Stockfish engine executable
        depth (int): Stockfish analysies depth
        multipv (int): Number of best engine lines to return
        max_workers (int): Number of Stockfish processes running at the same time

    Raises:
        AssertionError: If arguments with invalid types are provided.
    """

    def __init__(
        self,
        path: str,
        depth: Optional[int] = None,
        multipv: Optional[int] = None,
        max_workers: Optional[int] = None,
    ):
        assert isinstance(path, str), ["Invalid path type", path]
        assert isinstance(depth, Union[int, None]), ["Invalid depth type", depth]
        assert isinstance(multipv, Union[int, None]), ["Invalid multipv type", multipv]
        assert isinstance(max_workers, Union[int, None]), [
            "Invalid max_workers type",
            max_workers,
        ]

        if depth is None:
            depth = 18
        if multipv is None:
            multipv = 3
        if max_workers is None:
            threads = cpu_count()
            max_workers = max(1, threads - 2) if threads else 1

        self.path = path
        self.depth = depth
        self.multipv = multipv
        self.max_workers = max_workers

    async def analyze(self, initial_fen: str, uci_moves: list[str]) -> list[list[str]]:
        assert isinstance(initial_fen, str), ["Invalid initial_fen type", initial_fen]
        assert isinstance(uci_moves, list), ["Invalid uci_moves type", uci_moves]

        input_queue = SimpleQueue()
        analyses = []

        for i in range(len(uci_moves)):
            input_queue.put(uci_moves[: i + 1])

        async def run_worker() -> None:
            worker = StockfishWorker(self.path, self.depth, self.multipv)

            await worker.open()
            while not input_queue.empty():
                moves = input_queue.get()
                await worker.position(initial_fen, moves)
                before = perf_counter()
                analysis = await worker.go()
                analyses.append(analysis)
            await worker.close()

            return None

        async with TaskGroup() as tg:
            for _ in range(self.max_workers):
                tg.create_task(run_worker())

        return analyses


# class RemoteStockfishEngine:
# Todo
# ...


async def main():
    engine = LocalStockfishEngine("stockfish", 18, 1)
    print(engine.__dict__)
    before = perf_counter()
    analyses = await engine.analyze(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "g8f6", "e1g1", "f6e4", "f1e1"],
    )
    for analysis in analyses:
        print(analysis, end="\n\n")
    print("\n\nTime: ", perf_counter() - before)


if __name__ == "__main__":
    from asyncio import run

    run(main())

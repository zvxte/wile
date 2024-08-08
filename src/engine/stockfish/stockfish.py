from subprocess import SubprocessError
from typing import Optional, Union, Any
from os import cpu_count
from queue import SimpleQueue
from asyncio import TaskGroup

from ..error import EngineError
from .worker import StockfishEngineWorker


class LocalStockfishEngine:
    """
    Local Stockfish Engine

    Args:
        path (str): Path to Stockfish engine executable
        depth (int)
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
            max_workers = max(1, threads - 2) if threads is not None else 1

        self.path = path
        self.depth = depth
        self.multipv = multipv
        self.max_workers = max_workers

    async def analyze(self, initial_fen: str, uci_moves: list[str]) -> list[list[str]]:
        assert isinstance(initial_fen, str), ["Invalid initial_fen type", initial_fen]
        assert isinstance(uci_moves, list), ["Invalid uci_moves type", uci_moves]

        input_queue = SimpleQueue()
        analyses: list[Any] = [None] * (len(uci_moves) + 1)

        input_queue.put((0, [""]))
        for index in range(1, len(uci_moves) + 1):
            input_queue.put((index, uci_moves[: index]))

        async def run_worker() -> None:
            worker = StockfishEngineWorker(self.path, self.depth, self.multipv)

            await worker.open()
            while not input_queue.empty():
                index, moves = input_queue.get()
                await worker.position(initial_fen, moves)
                analysis = await worker.go()
                analyses[index] = analysis
            await worker.close()

            return None

        try:
            async with TaskGroup() as task_group:
                for _ in range(self.max_workers):
                    task_group.create_task(run_worker())
        except SubprocessError as e:
            raise EngineError(e)

        return analyses


# class RemoteStockfishEngine: ...  # TODO


async def main():
    engine = LocalStockfishEngine("stockfish", 16, 1, 10)
    print(engine.__dict__)
    before = perf_counter()
    # fmt: off
    analyses = await engine.analyze(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        [
            "e2e4", "e7e6", "d2d4", "a7a6", "a2a3", "d7d5", "b1c3", "d5e4", "c3e4", "h7h6", "g1f3", "f8e7", "c1f4", "g8f6", "f1d3",
            "b7b5", "e1g1", "c8b7", "f1e1", "b8d7", "d1d2", "c7c5", "c2c3", "c5c4", "d3c2", "d7b6", "a1d1", "b6d5", "f4g3", "f6h5",
            "f3e5", "d5f6", "d2e2", "d8d5", "f2f3", "h5g3", "h2g3", "d5d8", "g1f2", "f6e4", "c2e4", "b7e4", "e2e4", "e8g8", "e1h1",
            "e7f6", "e5g4", "d8e7", "g4h6", "g7h6", "h1h6", "f8d8", "d1h1", "a8c8", "h6h8", "f6h8", "e4h7", "g8f8", "h7h8",
        ],
    )
    # fmt: on
    print("\n\nTime: ", perf_counter() - before)


if __name__ == "__main__":
    from asyncio import run
    from time import perf_counter

    run(main())

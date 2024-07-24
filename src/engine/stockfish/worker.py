from subprocess import SubprocessError
from typing import Optional
from asyncio import create_subprocess_exec, wait_for
from asyncio.subprocess import PIPE, Process


class StockfishWorker:
    """Stockfish Engine Worker"""

    def __init__(self, path: str, depth: int = 18, multipv: int = 1):
        assert isinstance(path, str), ["Invalid path type", path]
        assert isinstance(depth, int), ["Invalid depth type", depth]
        assert isinstance(multipv, int), ["Invalid multipv type", multipv]

        self.path = path
        self.depth = depth
        self.multipv = multipv
        self._process: Optional[Process] = None

    async def open(self) -> None:
        """Opens Stockfish subprocess"""
        self._process = await create_subprocess_exec(
            program=self.path, stdin=PIPE, stdout=PIPE
        )
        if self._process.stdin is None or self._process.stdout is None:
            raise SubprocessError("Subprocess was created, but stdin or stdout is None")

        await self._write("uci\n")
        while True:
            line = await self._read()
            if line == "uciok":
                break
            if line is None:
                raise SubprocessError("Subprocess did not responded to uci command")

        # Set engine options
        await self._write(f"setoption name MultiPV value {self.multipv}\n")

    async def close(self):
        """Closes Stockfish subprocess"""
        await self._write("quit\n")
        if self._process:
            try:
                await wait_for(self._process.wait(), 1)
            except TimeoutError:
                self._process.terminate()

    async def position(self, initial_fen: str, uci_moves: list[str]) -> None:
        """Sets board position"""
        assert isinstance(initial_fen, str), ["Invalid initial_fen type", initial_fen]
        assert isinstance(uci_moves, list), ["Invalid uci_moves type", uci_moves]

        await self._write("isready\n")
        status = await self._read()
        if status == "readyok":
            await self._write(
                f"position fen {initial_fen} moves {" ".join(uci_moves)}\n"
            )
        else:
            raise SubprocessError("Subprocess did not responded to isready command")

    async def go(self) -> list[str]:
        """Analyzes position"""
        # Todo: Fix wrong result when analysing on higher depths
        await self._write(f"go depth {self.depth}\n")
        best_lines: list[str] = []
        pv_counter = 0
        while pv_counter < self.multipv:
            line = await self._read()
            if line is None:
                continue
            if line.startswith(f"info depth {self.depth} seldepth"):
                best_lines.append(line)
                pv_counter += 1
        return best_lines

    async def _read(self) -> Optional[str]:
        if self._process and self._process.stdout:
            try:
                line = await wait_for(self._process.stdout.readline(), 0.5)
                return line.decode().strip()
            except TimeoutError:
                return None

    async def _write(self, command: str) -> None:
        if self._process and self._process.stdin:
            self._process.stdin.write(command.encode())
            await self._process.stdin.drain()


async def main():
    worker = StockfishWorker("stockfish", 20, 3)
    await worker.open()
    await worker.position(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        ["e2e4", "e7e5", "g1f3"],
    )
    lines = await worker.go()
    await worker.close()
    for line in lines:
        print(line)


if __name__ == "__main__":
    from asyncio import run

    run(main())

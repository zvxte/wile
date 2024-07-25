from typing import Protocol, Iterable, Any


class Engine(Protocol):
    """Engine Interface"""

    async def analyze(self, initial_fen: str, uci_moves: Iterable[Any]) -> Iterable[Any]:
        """
        Analyzes chess game

        Args:
            initial_fen (str): Initial position in FEN.
            uci_moves (Iterable[Any]): Moves to analyze in UCI notation.

        Returns:
            Iterable[Any]: Analysis result.
        """
        raise NotImplementedError

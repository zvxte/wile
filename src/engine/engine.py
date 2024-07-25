from typing import Protocol, Iterable, Any


class Engine(Protocol):
    """Engine Interface"""

    async def analyze(self, uci_moves: Iterable[Any]) -> Iterable[Any]:
        """
        Analyzes chess game

        Args:
            uci_moves (Iterable[Any]): Moves to analyze in UCI notation.

        Returns:
            Iterable[Any]: Analysis result.
        """
        raise NotImplementedError

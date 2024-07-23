from typing import Protocol, Iterable, Any


class Engine(Protocol):
    """Engine Interface"""

    async def analyse(self, uci_moves: Iterable[Any]) -> Iterable[Any]:
        """
        Analyses chess game

        Args:
            uci_moves (Iterable[Any]): Moves to analyse in UCI notation.

        Returns:
            Iterable[Any]: Analysis result.
        """
        raise NotImplementedError

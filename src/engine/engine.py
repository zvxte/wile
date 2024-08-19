from typing import Protocol, Iterable, Any


class Engine(Protocol):
    """
    Engine Interface

    Engine implementations are responsible for communicating with chess engines
    to analyze chess positions. Analyzed positions should be later on parsed by
    appropriate analysis parser.
    """

    async def analyze(
        self, initial_fen: str, uci_moves: Iterable[str]
    ) -> Iterable[Any]:
        """
        Analyzes chess game

        Args:
            initial_fen (str)
            uci_moves (Iterable[str])

        Returns:
            Iterable[Any]: Result of analyzed positions.

        Raises:
            TypeError
            EngineError: If failed to run engine process; If failed to communicate with the engine process.
        """
        raise NotImplementedError

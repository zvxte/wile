from typing import Protocol


class Chess(Protocol):
    """Chess Library Interface"""

    def move(self, uci_move: str) -> None:
        """
        Makes a move

        Args:
            uci_move (str): Move in UCI notation.

        Returns:
            None

        Raises:
            ChessError
        """
        raise NotImplementedError

    def san_to_uci(self, san_move: str) -> str:
        """
        Converts from SAN to UCI notation used by many chess engines

        Args:
            san_move (str): Move in SAN notation.

        Returns:
            str: Move in UCI notation.

        Raises:
            ChessError
        """
        raise NotImplementedError

    def from_fen(self, fen: str) -> None:
        """
        Sets up board state from given FEN

        Args:
            fen (str): Position in FEN.

        Returns:
            None

        Raises:
            ChessError
        """
        raise NotImplementedError

    def to_fen(self) -> str:
        """
        Returns FEN of current board state

        Args:
            None

        Returns:
            str: Position in FEN.

        Raises:
            ChessError
        """
        raise NotImplementedError

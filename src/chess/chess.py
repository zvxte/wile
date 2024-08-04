from typing import Optional, Protocol

from chess import (
    STARTING_FEN,
    Board,
    InvalidMoveError,
    IllegalMoveError,
    AmbiguousMoveError,
)

from .error import ChessError


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
            AssertionError: If arguments with invalid types are provided.
            ChessError: If invalid move in uci notation is provided.
        """
        raise NotImplementedError

    def san_to_uci(self, san_move: str) -> str:
        """
        Converts from SAN to UCI notation

        Args:
            san_move (str): Move in SAN notation.

        Returns:
            str: Move in UCI notation.

        Raises:
            AssertionError: If arguments with invalid types are provided.
            ChessError: If invalid move in algebraic notation is provided.
        """
        raise NotImplementedError

    def from_fen(self, fen: str) -> None:
        """
        Sets up current position from given FEN

        Args:
            fen (str): Position in FEN.

        Returns:
            None

        Raises:
            AssertionError: If arguments with invalid types are provided.
            ChessError: If invalid FEN is provided.
        """
        raise NotImplementedError

    def to_fen(self) -> str:
        """
        Returns FEN of current position

        Args:
            None

        Returns:
            str: Position in FEN.
        """
        raise NotImplementedError


class ChessPy:
    """
    Chess Library in Python
    
    Args:
        fen (str): Position in FEN.
    
    Raises:
        AssertionError: If arguments with invalid types are provided.
    """

    def __init__(self, fen: Optional[str] = STARTING_FEN):
        assert isinstance(fen, str), ["Invalid fen type", fen]
        
        self.chessboard = Board(fen)

    def move(self, uci_move: str) -> None:
        assert isinstance(uci_move, str), ["Invalid uci_move type", uci_move]

        try:
            self.chessboard.push_uci(uci_move)
        except (ValueError, InvalidMoveError, IllegalMoveError) as e:
            raise ChessError(e)

    def san_to_uci(self, san_move: str) -> str:
        assert isinstance(san_move, str), ["Invalid san_move type", san_move]

        try:
            uci_move = self.chessboard.parse_san(san_move).uci()
            if uci_move == "0000":
                raise ChessError(f"Invalid SAN move {san_move}")
            return uci_move
        except (
            ValueError,
            InvalidMoveError,
            IllegalMoveError,
            AmbiguousMoveError,
        ) as e:
            raise ChessError(e)

    def from_fen(self, fen: str) -> None:
        assert isinstance(fen, str), ["Invalid fen type", fen]

        try:
            self.chessboard.set_fen(fen)
        except ValueError as e:
            raise ChessError(e)

    def to_fen(self) -> str:
        return self.chessboard.fen()

    def __repr__(self) -> str:
        return self.chessboard.__str__()


# class ChessC:
#     pass  # Not finished yet


if __name__ == "__main__":
    chess = ChessPy()
    fen = chess.to_fen()
    print(fen)
    uci_move = chess.san_to_uci("e4")
    print(uci_move)
    chess.move(uci_move)

    chess.from_fen("r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3")
    print(chess)

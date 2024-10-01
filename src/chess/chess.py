from typing import Protocol

from chess import (
    STARTING_FEN,
    Board,
    InvalidMoveError,
    IllegalMoveError,
    AmbiguousMoveError,
    WHITE,
    BLACK,
)

from .error import ChessError


class Chess(Protocol):
    """
    Chess Library Interface

    Chess library implementations are responsbile for converting
    move notations to interact with chess engines and generating FENs
    that are required by puzzles as a starting positions.
    """

    def move(self, uci_move: str) -> None:
        """
        Makes a move.

        Args:
            uci_move (str)

        Raises:
            TypeError
            ChessError: If move is illegal or invalid.
        """
        raise NotImplementedError

    def san_to_uci(self, san_move: str) -> str:
        """
        Converts from SAN to UCI notation.

        Args:
            san_move (str)

        Returns:
            str: Move in UCI notation.

        Raises:
            TypeError
            ChessError: If move is invalid.
        """
        raise NotImplementedError

    def uci_to_san(self, uci_move: str) -> str:
        """
        Converts from UCI notation to SAN.

        Args:
            uci_move (str)

        Returns:
            str: Move in SAN.

        Raises:
            TypeError
            ChessError: If move is invalid.
        """

        raise NotImplementedError

    def from_fen(self, fen: str) -> None:
        """
        Sets up current position from given FEN.

        Args:
            fen (str)

        Raises:
            TypeError
            ChessError: If FEN is invalid.
        """
        raise NotImplementedError

    def to_fen(self) -> str:
        """
        Returns FEN of current position.

        Returns:
            str: Position in FEN.
        """
        raise NotImplementedError

    def color(self) -> int:
        """
        Returns current side.

        Returns:
            int: 0 for white, 1 for black.
        """
        raise NotImplementedError


class ChessPy:
    def __init__(self):
        self.chessboard = Board()

    def move(self, uci_move: str) -> None:
        if not isinstance(uci_move, str):
            raise TypeError("Invalid argument types", type(uci_move))

        try:
            self.chessboard.push_uci(uci_move)
        except (ValueError, InvalidMoveError, IllegalMoveError) as e:
            raise ChessError(e)

    def san_to_uci(self, san_move: str) -> str:
        if not isinstance(san_move, str):
            raise TypeError("Invalid argument types", type(san_move))

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

    def uci_to_san(self, uci_move: str) -> str:
        if not isinstance(uci_move, str):
            raise TypeError("Invalid argument types", type(uci_move))

        try:
            move = self.chessboard.parse_uci(uci_move)
            return self.chessboard.san(move)

        except (
            ValueError,
            InvalidMoveError,
            IllegalMoveError,
        ) as e:
            raise ChessError(e)

    def from_fen(self, fen: str) -> None:
        if not isinstance(fen, str):
            raise TypeError("Invalid argument types", type(fen))

        try:
            self.chessboard.set_fen(fen)
        except ValueError as e:
            raise ChessError(e)

    def to_fen(self) -> str:
        return self.chessboard.fen()

    def color(self) -> int:
        return 0 if self.chessboard.turn == WHITE else 1

    def __repr__(self) -> str:
        return self.chessboard.__str__()


if __name__ == "__main__":
    chess = ChessPy()
    fen = chess.to_fen()
    print(fen)
    uci_move = chess.san_to_uci("e4")
    print(uci_move)
    chess.move(uci_move)

    chess.from_fen("r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3")
    print(chess)

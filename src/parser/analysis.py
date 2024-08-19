from typing import Protocol, Any

from src.models.move import UciMove

from ..models import Analysis, Color, Score, ScoreName, Move, SanMove, UciMove
from ..chess import ChessPy, ChessError
from .error import ParserError


class AnalysisParser(Protocol):
    """Analysis Parser Interface"""

    def parse(
        self, analysis_line: Any, initial_fen: str, moves: list[Move]
    ) -> Analysis:
        """
        Parses analysis line

        Args:
            analysis_line (Any)
            initial_fen (str)
            moves (list[Move]): Moves that were played in order to achieve current position.
                                Needed to correctly convert best move from UCI notation into SAN, but also to
                                determine player's side to convert relative score values into absolute.

        Returns:
            Analysis

        Raises:
            TypeError
            ValueError
            ParserError
        """
        raise NotImplementedError


class StockfishAnalysisParser:
    def __init__(self):
        self.chessboard = ChessPy()

    def parse(
        self, analysis_line: str, initial_fen: str, moves: list[Move]
    ) -> Analysis:
        # example:
        # info depth 25 seldepth 31 multipv 1 score cp 33 nodes 4464545 nps 1267256
        # hashfull 937 tbhits 0 time 3523 pv e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6
        # e1g1 f6e4 d2d4 b7b5 a4b3 d7d5 d4e5 c8e6 c2c3 f8e7 b3c2 e6g4 f1e1 e8g8 b1d2
        # c6e5 d2e4 g4f3 g2f3 d5e4 c2e4

        if not isinstance(analysis_line, str) or not isinstance(moves, list):
            raise TypeError("Invalid argument types")

        uci_move, multipv, score_name, score_value = None, None, None, None
        parts = analysis_line.split(" ")
        try:
            for i, part in enumerate(parts):
                if part == "multipv":
                    multipv = int(parts[i + 1])
                elif part == "score":
                    score_name = parts[i + 1]
                    score_value = int(parts[i + 2])
                elif part == "pv":
                    uci_move = parts[i + 1]
                    break
        except (IndexError, ValueError) as e:
            raise ParserError(e)

        if (
            uci_move is None
            or multipv is None
            or score_name is None
            or score_value is None
        ):
            raise ParserError("Invalid analysis line")

        try:
            self.chessboard.from_fen(initial_fen)
            for move in moves:
                self.chessboard.move(move.uci_move.value)
            san_move = self.chessboard.uci_to_san(uci_move)
            side = Color(self.chessboard.color())
            move = Move(SanMove(san_move), UciMove(uci_move), side)
        except (ChessError, TypeError, ValueError) as e:
            raise ParserError(e)

        if side == Color.BLACK:
            score_value *= -1

        if score_name == ScoreName.CP.value:
            score_name = ScoreName.CP
        elif score_name == ScoreName.MATE.value:
            score_name = ScoreName.MATE
        else:
            raise ParserError("Invalid score name")

        return Analysis(
            move=move, multipv=multipv, score=Score(score_name, score_value)
        )


if __name__ == "__main__":
    analysis_line = "info depth 25 seldepth 31 multipv 1 score cp 33 nodes 4464545 nps 1267256 hashfull 937 tbhits 0 time 3523 pv e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f6e4 d2d4 b7b5 a4b3 d7d5 d4e5 c8e6 c2c3 f8e7 b3c2 e6g4 f1e1 e8g8 b1d2 c6e5 d2e4 g4f3 g2f3 d5e4 c2e4"
    parser = StockfishAnalysisParser()
    analysis = parser.parse(
        analysis_line, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []
    )
    print(analysis)

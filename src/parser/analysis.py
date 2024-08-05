from typing import Protocol, Any

from ..models import Analysis, Color, Score, ScoreName
from .error import ParserError


class AnalysisParser(Protocol):
    """Analysis Parser Interface"""

    def parse(self, analysis: Any, side: Color) -> Analysis:
        """
        Parses analysis result

        Args:
            analysis (Any): Analysis to parse.
            side (Color): Player's side. Used to convert relative values into absolute.

        Returns:
            Analysis: Parsed analysis.

        Raises:
            AssertionError: If arguments with invalid types are provided.
            ParserError: If failed to parse analysis.
        """
        raise NotImplementedError


class StockfishAnalysisParser:
    def parse(self, analysis: str, side: Color) -> Analysis:
        # example:
        # info depth 25 seldepth 31 multipv 1 score cp 33 nodes 4464545 nps 1267256
        # hashfull 937 tbhits 0 time 3523 pv e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6
        # e1g1 f6e4 d2d4 b7b5 a4b3 d7d5 d4e5 c8e6 c2c3 f8e7 b3c2 e6g4 f1e1 e8g8 b1d2
        # c6e5 d2e4 g4f3 g2f3 d5e4 c2e4

        assert isinstance(analysis, str), ["Invalid analysis type", analysis]
        assert isinstance(side, Color), ["Invalid side type", side]

        uci_move, multipv, score_name, score_value = None, None, None, None
        parts = analysis.split(" ")
        try:
            for i, part in enumerate(parts):
                if part == "pv":
                    uci_move = parts[i + 1]
                elif part == "multipv":
                    multipv = int(parts[i + 1])
                elif part == "score":
                    score_name = parts[i + 1]
                    score_value = int(parts[i + 2])
        except (IndexError, ValueError) as e:
            raise ParserError(e)

        assert isinstance(uci_move, str), ["Invalid uci_move type", uci_move]
        assert isinstance(multipv, int), ["Invalid multipv type", multipv]
        assert isinstance(score_name, str), ["Invalid score_name type", score_name]
        assert isinstance(score_value, int), ["Invalid score_value type", score_value]

        if side == Color.BLACK:
            score_value *= -1

        if score_name == ScoreName.CP.value:
            score_name = ScoreName.CP
        elif score_name == ScoreName.MATE.value:
            score_name = ScoreName.MATE
        else:
            raise ParserError("Invalid score name")

        return Analysis(
            uci_move=uci_move,
            multipv=multipv,
            score=Score(score_name, score_value)
        )


if __name__ == "__main__":
    analysis_line = "info depth 25 seldepth 31 multipv 1 score cp 33 nodes 4464545 nps 1267256 hashfull 937 tbhits 0 time 3523 pv e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f6e4 d2d4 b7b5 a4b3 d7d5 d4e5 c8e6 c2c3 f8e7 b3c2 e6g4 f1e1 e8g8 b1d2 c6e5 d2e4 g4f3 g2f3 d5e4 c2e4"
    parser = StockfishAnalysisParser()
    analysis = parser.parse(analysis_line, Color.WHITE)
    print(analysis)

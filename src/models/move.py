from typing import Optional, Union

from .analysis import Analysis
from .score import Score
from .color import Color


class Move:
    """
    Represents chess move

    Raises:
        AssertionError: If arguments with invalid types are provided.
        ValueError: If argument values are falsy.
    """

    def __init__(
        self,
        san_move: str,
        uci_move: Optional[str] = None,
        side: Optional[Color] = None,
        score: Optional[Score] = None,
        analyses: Optional[list[Analysis]] = None,
    ):
        assert isinstance(san_move, str), ["Invalid san_move type", san_move]
        assert isinstance(uci_move, Union[str, None]), [
            "Invalid uci_move type",
            uci_move,
        ]
        assert isinstance(side, Union[Color, None]), ["Invalid side type", side]
        assert isinstance(score, Union[Score, None]), ["Invalid score_name type", score]
        assert isinstance(analyses, Union[list, None]), [
            "Invalid analyses type",
            analyses,
        ]

        if not san_move:
            raise ValueError("Invalid arguments")

        self.san_move = san_move
        self.uci_move = uci_move
        self.side = side
        self.score = score
        self.analyses = analyses

    def __repr__(self) -> str:
        return f"Move(\n{self.san_move}\n{self.uci_move}\n{self.side}\n{self.score}\n{self.analyses}\n)"

from typing import Optional, Union

from .analysis import Analysis


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
        score_name: Optional[str] = None,
        score_value: Optional[int] = None,
        analyses: Optional[list[Analysis]] = None,
    ):
        assert isinstance(san_move, str), ["Invalid san_move type", san_move]
        assert isinstance(uci_move, Union[str, None]), [
            "Invalid uci_move type",
            uci_move,
        ]
        assert isinstance(score_name, Union[str, None]), [
            "Invalid score_name type",
            score_name,
        ]
        assert isinstance(score_value, Union[int, None]), [
            "Invalid score_value type",
            score_value,
        ]
        assert isinstance(analyses, Union[list, None]), [
            "Invalid analyses type",
            analyses,
        ]

        if not san_move:
            raise ValueError("Invalid arguments")

        self.san_move = san_move
        self.uci_move = uci_move
        self.analyses = analyses

    def __repr__(self) -> str:
        return f"Move({self.san_move}, {self.uci_move}, {self.analyses})"

from typing import Optional, Union

from .analysis import Analysis


class Move:
    """
    Represents chess move

    Raises:
        AssertionError: If arguments with invalid types are provided.
    """
    def __init__(self, san_move: str, uci_move: Optional[str] = None, analyses: Optional[list[Analysis]] = None):
        assert isinstance(san_move, str), ["Invalid san_move type", san_move]
        assert isinstance(uci_move, Union[str, None]), ["Invalid uci_move type", uci_move]
        assert isinstance(analyses, Union[list, None]), ["Invalid analyses type", analyses]

        self.san_move = san_move
        self.uci_move = uci_move
        self.analyses = analyses

from .score import ScoreName


class Analysis:
    """
    Represents engine analysis

    Raises:
        AssertionError: If arguments with invalid types are provided.
        ValueError: If argument values are falsy.
    """

    def __init__(self, uci_move: str, multipv: int, score_name: ScoreName, score_value: int):
        assert isinstance(uci_move, str), ["Invalid uci_move type", uci_move]
        assert isinstance(multipv, int), ["Invalid multipv type", multipv]
        assert isinstance(score_name, ScoreName), ["Invalid score_name type", score_name]
        assert isinstance(score_value, int), ["Invalid score_value type", score_value]

        if not uci_move:
            raise ValueError("Invalid arguments")

        self.uci_move = uci_move
        self.multipv = multipv
        self.score_name = score_name
        self.score_value = score_value

    def __repr__(self) -> str:
        return f"Analysis({self.uci_move}, {self.multipv}, {self.score_name}, {self.score_value})"

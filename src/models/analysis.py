from .score import Score


class Analysis:
    """
    Represents engine analysis

    Raises:
        AssertionError: If arguments with invalid types are provided.
        ValueError: If argument values are falsy.
    """

    def __init__(self, uci_move: str, multipv: int, score: Score):
        assert isinstance(uci_move, str), ["Invalid uci_move type", uci_move]
        assert isinstance(multipv, int), ["Invalid multipv type", multipv]
        assert isinstance(score, Score), ["Invalid score type", score]

        if not uci_move:
            raise ValueError("Invalid arguments")

        self.uci_move = uci_move
        self.multipv = multipv
        self.score = score

    def __repr__(self) -> str:
        return f"Analysis({self.uci_move}, {self.multipv}, {self.score})"

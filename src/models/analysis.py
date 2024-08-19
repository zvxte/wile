from .score import Score
from .move import Move


class Analysis:
    """
    Represents engine analysis line

    Raises:
        TypeError
        ValueError
    """

    def __init__(self, move: Move, multipv: int, score: Score):
        if (
            not isinstance(move, Move)
            or not isinstance(multipv, int)
            or not isinstance(score, Score)
        ):
            raise TypeError("Invalid argument types")

        self.move = move
        self.multipv = multipv
        self.score = score

    def __repr__(self) -> str:
        return f"Analysis({self.move}, {self.multipv}, {self.score})"

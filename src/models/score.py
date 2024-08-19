from enum import Enum


class ScoreName(Enum):
    CP = "cp"
    MATE = "mate"


class Score:
    """
    Represents analysis score
    
    Raises:
        TypeError
    """
    def __init__(self, score_name: ScoreName, score_value: int):
        if not isinstance(score_name, ScoreName) or not isinstance(score_value, int):
            raise TypeError("Invalid argument types")
        
        self.score_name = score_name
        self.score_value = score_value

    def __repr__(self) -> str:
        return f"Score({self.score_name}, {self.score_value})"

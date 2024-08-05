from enum import Enum


class ScoreName(Enum):
    CP = "cp"
    MATE = "mate"


class Score:
    """
    Represents analysis score
    
    Raises:
        AssertionError: If arguments with invalid types are provided.
    """
    def __init__(self, score_name: ScoreName, score_value: int):
        assert isinstance(score_name, ScoreName), ["Invalid score_name type", score_name]
        assert isinstance(score_value, int), ["Invalid score_value type", score_value]
        
        self.score_name = score_name
        self.score_value = score_value

    def __repr__(self) -> str:
        return f"Score({self.score_name}, {self.score_value})"

from .move import Move
from .score import Score
from .analysis import Analysis
from .platform import Platform
from .player import Player
from .color import Color


class Puzzle:
    """
    Represents chess puzzle

    Raises:
        TypeError
        ValueError
    """

    def __init__(
        self,
        fen: str,
        move: Move,
        score: Score,
        best_lines: list[Analysis],
        game_id: str,
        platform: Platform,
        url: str,
        white: Player,
        black: Player,
        side: Color,
    ):
        if (
            not isinstance(fen, str)
            or not isinstance(move, Move)
            or not isinstance(score, Score)
            or not isinstance(best_lines, list)
            or not isinstance(game_id, str)
            or not isinstance(platform, Platform)
            or not isinstance(url, str)
            or not isinstance(white, Player)
            or not isinstance(black, Player)
            or not isinstance(side, Color)
        ):
            raise TypeError("Invalid argument types")

        if not fen or not game_id or not url:
            raise ValueError("Invalid argument values")

        self.fen = fen
        self.move = move
        self.score = score
        self.best_lines = best_lines
        self.game_id = game_id
        self.platform = platform
        self.url = url
        self.white = white
        self.black = black
        self.side = side

    def __repr__(self) -> str:
        return f"Puzzle(\n{self.fen}\n{self.move}\n{self.score}\n{self.best_lines}\n{self.game_id}\n{self.platform}\n{self.url}\n{self.white}\n{self.black}\n{self.side}\n)"

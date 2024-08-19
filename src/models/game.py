from .platform import Platform
from .player import Player
from .color import Color
from .move import Move
from .analysis import Analysis


class Game:
    """
    Represents chess game

    Raises:
        TypeError
        ValueError
    """

    def __init__(
        self,
        game_id: str,
        platform: Platform,
        url: str,
        white: Player,
        black: Player,
        side: Color,
        initial_fen: str,
        moves: list[Move],
        analyses: list[list[Analysis]] | None = None,
    ):
        if (
            not isinstance(game_id, str)
            or not isinstance(platform, Platform)
            or not isinstance(url, str)
            or not isinstance(white, Player)
            or not isinstance(black, Player)
            or not isinstance(side, Color)
            or not isinstance(initial_fen, str)
            or not isinstance(moves, list)
            or not isinstance(analyses, list | None)
        ):
            raise TypeError("Invalid argument types")

        if not game_id or not url or not initial_fen or not moves:
            raise ValueError("Invalid argument values")

        self.game_id = game_id
        self.platform = platform
        self.url = url
        self.white = white
        self.black = black
        self.side = side
        self.initial_fen = initial_fen
        self.moves = moves
        self.analyses = analyses

    def __repr__(self) -> str:
        return f"Game(\n{self.game_id}\n{self.platform}\n{self.url}\n{self.white}\n{self.black}\n{self.side}\n{self.initial_fen}\n{self.moves}\n{self.analyses}\n)"

from .move import Move
from .player import Player
from .color import Color
from .platform import Platform


class Puzzle:
    """
    Represents chess puzzle

    Raises:
        AssertionError: If arguments with invalid types are provided.
        ValueError: If argument values are falsy.
    """

    def __init__(
        self,
        fen: str,
        move: Move,
        game_id: str,
        platform: Platform,
        url: str,
        white: Player,
        black: Player,
        side: Color,
    ):
        assert isinstance(fen, str), ["Invalid fen type", fen]
        assert isinstance(move, Move), ["Invalid move type", move]
        assert isinstance(game_id, str), ["Invalid game_id type", game_id]
        assert isinstance(platform, Platform), ["Invalid platform type", platform]
        assert isinstance(url, str), ["Invalid url type", url]
        assert isinstance(white, Player), ["Invalid white type", white]
        assert isinstance(black, Player), ["Invalid black type", black]
        assert isinstance(side, Color), ["Invalid side type", side]

        if not fen or not game_id or not url:
            raise ValueError

        self.fen = fen
        self.move = move
        self.game_id = game_id
        self.platform = platform
        self.url = url
        self.white = white
        self.black = black
        self.side = side

    def __repr__(self) -> str:
        return f"Puzzle(\n{self.fen}\n{self.move}\n{self.game_id}\n{self.platform}\n{self.url}\n{self.white}\n{self.black}\n{self.side}\n)"

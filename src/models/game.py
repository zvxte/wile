from .player import Player
from .move import Move
from .color import Color
from .platform import Platform


class Game:
    """
    Represents chess game
    
    Raises:
        AssertionError: If arguments with invalid types are provided.
        ValueError: If argument values are falsy.
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
        moves: list[Move]
    ):
        assert isinstance(game_id, str), ["Invalid game_id type", game_id]
        assert isinstance(platform, Platform), ["Invalid platform type", platform]
        assert isinstance(url, str), ["Invalid url type", url]
        assert isinstance(white, Player), ["Invalid white type", white]
        assert isinstance(black, Player), ["Invalid black type", black]
        assert isinstance(side, Color), ["Invalid side type", side]
        assert isinstance(initial_fen, str), ["Invalid initial_fen type", initial_fen]
        assert isinstance(moves, list), ["Invalid moves type", moves]

        if not game_id or not url or not initial_fen or not moves:
            raise ValueError("Invalid arguments")

        self.game_id = game_id
        self.platform = platform
        self.url = url
        self.white = white
        self.black = black
        self.side = side
        self.initial_fen = initial_fen
        self.moves = moves

    def __repr__(self) -> str:
        return f"Game(\n{self.game_id}\n{self.platform}\n{self.url}\n{self.white}\n{self.black}\n{self.side}\n{self.initial_fen}\n{self.moves}\n)"

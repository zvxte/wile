from typing import Optional
from .player import Player


class Game:
    """
    Represents chess game
    
    Raises:
        AssertionError: If arguments with invalid types are provided.
        ValueError: If str arguments are empty.
    """

    def __init__(
        self,
        game_id: str,
        platform: str,
        url: str,
        white: Player,
        black: Player,
        initial_fen: str,
        san_moves: Optional[list[str]] = None,
        uci_moves: Optional[list[str]] = None,
    ):
        assert isinstance(game_id, str), ["Invalid game_id type", game_id]
        assert isinstance(platform, str), ["Invalid platform type", platform]
        assert isinstance(url, str), ["Invalid url type", url]
        assert isinstance(white, Player), ["Invalid white type", white]
        assert isinstance(black, Player), ["Invalid black type", black]
        assert isinstance(initial_fen, str), ["Invalid initial_fen type", initial_fen]

        if not game_id or not platform or not url or not initial_fen:
            raise ValueError("Invalid arguments")
        self.game_id = game_id
        self.platform = platform
        self.url = url
        self.white = white
        self.black = black
        self.initial_fen = initial_fen
        self.san_moves = san_moves
        self.uci_moves = uci_moves

    def __repr__(self) -> str:
        return f"Game(\n{self.game_id}\n{self.platform}\n{self.url}\n{self.white}\n{self.black}\n{self.initial_fen}\n{self.san_moves}\n{self.uci_moves}\n)"

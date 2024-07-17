from .player import Player


class Game:
    def __init__(
        self,
        game_id: str,
        platform: str,
        url: str,
        white: Player,
        black: Player,
        initial_fen: str,
        moves: list[str],
    ):
        if (
            not game_id
            or not platform
            or not url
            or not white
            or not black
            or not initial_fen
            or not moves
        ):
            raise ValueError("Invalid arguments")
        self.game_id = game_id
        self.platform = platform
        self.url = url
        self.white = white
        self.black = black
        self.initial_fen = initial_fen
        self.moves = moves

    def __repr__(self) -> str:
        return f"Game({self.game_id}, {self.platform}, {self.url}, {self.white}, {self.black}, {self.initial_fen}, {self.moves})"

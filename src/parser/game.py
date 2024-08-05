from typing import Protocol, Any

from .error import ParserError
from .utils import parse_pgn_moves
from ..models import Game, Player, Move, Color, Platform


class GameParser(Protocol):
    """Game Parser Interface"""

    def parse(self, game: Any, username: str) -> Game:
        """
        Parses chess game

        Args:
            game (Any): Game to parse.
            username (str): Username to determine player's side.

        Returns:
            Game: Parsed game.

        Raises:
            AssertionError: If arguments with invalid types are provided.
            ParserError: If failed to parse game.
        """
        raise NotImplementedError


class ChessComGameParser:
    def parse(self, game: dict[str, Any], username: str) -> Game:
        assert isinstance(game, dict), ["Invalid game type", game]
        assert isinstance(username, str), ["Invalid username type", username]

        moves = [Move(san_move) for san_move in parse_pgn_moves(game["pgn"])]
        for (i, move) in enumerate(moves):
            move.side = Color.WHITE if i % 2 == 0 else Color.BLACK
        
        white = Player(
            username=game["white"]["username"], rating=game["white"]["rating"]
        )
        black = Player(
            username=game["black"]["username"], rating=game["black"]["rating"]
        )
    
        if white.username.lower() == username.lower():
            side = Color.WHITE
        elif black.username.lower() == username.lower():
            side = Color.BLACK
        else:
            raise ParserError("Invalid username")

        try:
            return Game(
                game_id=game["uuid"],
                platform=Platform.CHESSCOM,
                url=game["url"],
                white=white,
                black=black,
                side=side,
                initial_fen=game["initial_setup"],
                moves=moves,
            )
        except (KeyError, ValueError) as e:
            raise ParserError(e)


async def main():
    # testing
    fetcher = ChessComFetcher()
    games = await fetcher.fetch("hikaru", 1721088000)  # since July 16, 2024

    parser = ChessComGameParser()
    for game in games[:5]:
        print(parser.parse(game, "hikaru"), end="\n\n")


if __name__ == "__main__":
    from asyncio import run
    from ..fetcher import ChessComFetcher

    run(main())

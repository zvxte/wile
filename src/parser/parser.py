from typing import Protocol, Any

from .error import ParserError
from .utils import parse_pgn_moves
from ..models import Game, Player


class Parser(Protocol):
    """Parser Interface"""

    def parse(self, game: Any) -> Game:
        """
        Parses chess game

        Args:
            game (Any): Game to parse. Type depends on specific implementation.

        Returns:
            Game: Parsed game.

        Raises:
            ParserError
        """
        raise NotImplementedError


class ChessComParser:
    def parse(self, game: dict[str, Any]) -> Game:
        try:
            return Game(
                game_id=game["uuid"],
                platform="Chess.com",
                url=game["url"],
                white=Player(
                    username=game["white"]["username"], rating=game["white"]["rating"]
                ),
                black=Player(
                    username=game["black"]["username"], rating=game["black"]["rating"]
                ),
                initial_fen=game["initial_setup"],
                moves=parse_pgn_moves(game["pgn"]),
            )
        except KeyError or ValueError as e:
            raise ParserError(e)


async def main():
    # testing
    fetcher = ChessComFetcher()
    games = await fetcher.fetch("hikaru", 1721088000)  # since July 16, 2024

    parser = ChessComParser()
    for game in games[:5]:
        print(parser.parse(game), end="\n\n")


if __name__ == "__main__":
    from asyncio import run
    from ..fetcher import ChessComFetcher

    run(main())

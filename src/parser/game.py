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
            game (Any)
            username (str): Username to determine player's side.

        Returns:
            Game

        Raises:
            AssertionError: If arguments with invalid types are provided.
            ParserError
        """
        raise NotImplementedError


class ChessComGameParser:
    def parse(self, game: dict[str, Any], username: str) -> Game:
        assert isinstance(game, dict), ["Invalid game type", game]
        assert isinstance(username, str), ["Invalid username type", username]

        moves = [Move(san_move) for san_move in parse_pgn_moves(game["pgn"])]
        for i, move in enumerate(moves):
            move.side = Color.WHITE if i % 2 == 0 else Color.BLACK

        try:
            white = Player(
                username=game["white"]["username"], rating=game["white"]["rating"]
            )
            black = Player(
                username=game["black"]["username"], rating=game["black"]["rating"]
            )
        except KeyError as e:
            raise ParserError(e)

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


class LichessGameParser:
    def parse(self, game: Any, username: str) -> Game:
        assert isinstance(game, dict), ["Invalid game type", game]
        assert isinstance(username, str), ["Invalid username type", username]

        try:
            moves = [Move(san_move) for san_move in game["moves"].split(" ")]
            white = Player(
                game["players"]["white"]["user"]["name"],
                game["players"]["white"]["rating"],
            )
            black = Player(
                game["players"]["black"]["user"]["name"],
                game["players"]["black"]["rating"],
            )
        except KeyError as e:
            raise ParserError(e)

        for i, move in enumerate(moves):
            move.side = Color.WHITE if i % 2 == 0 else Color.BLACK

        if white.username.lower() == username.lower():
            side = Color.WHITE
        elif black.username.lower() == username.lower():
            side = Color.BLACK
        else:
            raise ParserError("Invalid username")

        initial_fen = game.get("initialFen")
        if initial_fen is None:
            initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        return Game(
            game_id=game["id"],
            platform=Platform.LICHESS,
            url=f"https://lichess.org/{game["id"]}",
            white=white,
            black=black,
            side=side,
            initial_fen=initial_fen,
            moves=moves,
        )


async def main():
    # testing
    # chesscom_fetcher = ChessComFetcher()
    # chesscom_games = await chesscom_fetcher.fetch("hikaru", 1721088000)  # since July 16, 2024

    # chesscom_parser = ChessComGameParser()
    # for game in chesscom_games[:5]:
    #     print(chesscom_parser.parse(game, "hikaru"), end="\n\n")

    lichess_fetcher = LichessFetcher()
    lichess_parser = LichessGameParser()
    lichess_games = await lichess_fetcher.fetch("czarnov", 1723208004, 1723380804)
    for game in lichess_games:
        print(lichess_parser.parse(game, "czarnov"))


if __name__ == "__main__":
    from asyncio import run
    from ..fetcher import ChessComFetcher, LichessFetcher

    run(main())

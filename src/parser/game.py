from typing import Protocol, Any

from .error import ParserError
from .utils import parse_pgn_moves
from ..models import Game, Player, Move, SanMove, UciMove, Color, Platform
from ..chess import ChessPy, ChessError


class GameParser(Protocol):
    """Game Parser Interface"""

    def parse(self, game: Any, username: str) -> Game:
        """
        Parses chess game

        Args:
            game (Any)
            username (str): Needed to determine player's side.

        Returns:
            Game

        Raises:
            TypeError
            ParserError
        """
        raise NotImplementedError


class ChessComGameParser:
    def __init__(self):
        self.chessboard = ChessPy()

    def parse(self, game: dict[str, Any], username: str) -> Game:
        if not isinstance(game, dict) or not isinstance(username, str):
            raise TypeError("Invalid argument types")

        try:
            game_id = game["uuid"]
            initial_fen = game["initial_setup"]
            url = game["url"]
            white = Player(
                username=game["white"]["username"], rating=game["white"]["rating"]
            )
            black = Player(
                username=game["black"]["username"], rating=game["black"]["rating"]
            )

        except KeyError as e:
            raise ParserError(e)

        san_moves = parse_pgn_moves(game["pgn"])
        moves: list[Move] = []
        try:
            self.chessboard.from_fen(initial_fen)
            for san_move in san_moves:
                uci_move = self.chessboard.san_to_uci(san_move)
                side = Color(self.chessboard.color())
                moves.append(Move(SanMove(san_move), UciMove(uci_move), side))
                self.chessboard.move(uci_move)
        except (ChessError, TypeError, ValueError) as e:
            raise ParserError(e)

        if white.username.lower() == username.lower():
            side = Color.WHITE
        elif black.username.lower() == username.lower():
            side = Color.BLACK
        else:
            raise ParserError("Invalid username")

        try:
            return Game(
                game_id=game_id,
                platform=Platform.CHESSCOM,
                url=url,
                white=white,
                black=black,
                side=side,
                initial_fen=initial_fen,
                moves=moves,
                analyses=None,
            )
        except (TypeError, ValueError) as e:
            raise ParserError(e)


class LichessGameParser:
    def __init__(self):
        self.chessboard = ChessPy()

    def parse(self, game: Any, username: str) -> Game:
        assert isinstance(game, dict), ["Invalid game type", game]
        assert isinstance(username, str), ["Invalid username type", username]

        try:
            game_id = game["id"]
            url = f"https://lichess.org/{game["id"]}"
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

        initial_fen = game.get("initialFen")
        if initial_fen is None:
            initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        san_moves = game["moves"].split(" ")
        moves: list[Move] = []
        try:
            self.chessboard.from_fen(initial_fen)
            for san_move in san_moves:
                uci_move = self.chessboard.san_to_uci(san_move)
                side = Color(self.chessboard.color())
                moves.append(Move(SanMove(san_move), UciMove(uci_move), side))
                self.chessboard.move(uci_move)
        except (ChessError, TypeError, ValueError) as e:
            raise ParserError(e)

        if white.username.lower() == username.lower():
            side = Color.WHITE
        elif black.username.lower() == username.lower():
            side = Color.BLACK
        else:
            raise ParserError("Invalid username")

        try:
            return Game(
                game_id=game_id,
                platform=Platform.LICHESS,
                url=url,
                white=white,
                black=black,
                side=side,
                initial_fen=initial_fen,
                moves=moves,
                analyses=None,
            )
        except (TypeError, ValueError) as e:
            raise ParserError(e)


async def main():
    # testing
    # chesscom_fetcher = ChessComFetcher()
    # chesscom_games = await chesscom_fetcher.fetch(
    #     "hikaru", 1721088000
    # )  # since July 16, 2024

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

from typing import Protocol, Iterable

from src.chess.chess import ChessPy
from src.models.score import ScoreName

from ..models import Game, Puzzle, Color


class PuzzleCreator(Protocol):
    """
    Puzzle Creator Interface

    Puzzle creator implementations are responsible for creating
    chess puzzles based on some rules. Moves of a given game
    should be already analyzed before invoking any methods or
    creator will always return empty iterable, but single
    not analyzed moves will mostly not interrupt.
    """

    def create(self, game: Game) -> Iterable[Puzzle]:
        """
        Creates chess puzzles

        Args:
            game (Game)

        Returns:
            Iterable[Puzzle]: All found puzzles. Could be empty.
        """
        raise NotImplementedError


class AnalysisBasedPuzzleCreator:
    """Creates chess puzzles based purely on engine's analysis"""

    def __init__(self):
        self.chess = ChessPy()

    def create(self, game: Game) -> list[Puzzle]:
        puzzles: list[Puzzle] = []
        start = 10 if game.side == Color.WHITE else 11

        for i in range(start, len(game.moves) - 1, 2):
            move = game.moves[i]
            if move.score is None or move.analyses is None:
                continue
            best_line = move.analyses[0]
            if (
                move.score.score_name == ScoreName.CP
                and best_line.score.score_name == ScoreName.CP
            ):
                if (
                    -400 < move.score.score_value < 400
                    and abs(move.score.score_value) - abs(best_line.score.score_value)
                    > 100
                ):
                    self.chess.from_fen(game.initial_fen)
                    uci_moves = [move.uci_move for move in game.moves[:i]]
                    for uci_move in uci_moves:
                        if uci_move is None:
                            return puzzles
                        self.chess.move(uci_move)
                    fen = self.chess.to_fen()
                    puzzles.append(
                        Puzzle(
                            fen=fen,
                            move=move,
                            game_id=game.game_id,
                            platform=game.platform,
                            url=game.url,
                            white=game.white,
                            black=game.black,
                            side=game.side,
                        )
                    )
        return puzzles


async def main():
    from ..fetcher import ChessComFetcher
    from ..parser import ChessComGameParser, StockfishAnalysisParser
    from ..chess import ChessPy
    from ..engine.stockfish import LocalStockfishEngine
    from ..models import Analysis

    fetcher = ChessComFetcher()
    game_parser = ChessComGameParser()
    fetched_games = await fetcher.fetch("hikaru", 1720908000)
    games = [game_parser.parse(game, "hikaru") for game in fetched_games][:4]

    chessboard = ChessPy()
    for game in games:
        chessboard.from_fen(game.initial_fen)
        for move in game.moves:
            uci_move = chessboard.san_to_uci(move.san_move)
            move.uci_move = uci_move
            chessboard.move(uci_move)

    engine = LocalStockfishEngine("stockfish", depth=18, multipv=1, max_workers=10)
    analysis_parser = StockfishAnalysisParser()

    for game in games:
        uci_moves = [move.uci_move for move in game.moves]
        engine_result = await engine.analyze(game.initial_fen, [""] + uci_moves)
        for i in range(len(game.moves)):
            move = game.moves[i]
            analyses = [
                analysis_parser.parse(analysis, move.side)
                for analysis in engine_result[i]
            ]
            move.analyses = [] + analyses
            if i > 0:
                game.moves[i - 1].score = analyses[0].score

    for game in games:
        print("GAME: ", game, "\n\n")

    creator = AnalysisBasedPuzzleCreator()
    puzzles = [creator.create(game) for game in games]

    for puzzle in puzzles:
        print(puzzle, "\n\n")


if __name__ == "__main__":
    from asyncio import run

    run(main())

from typing import Protocol, Iterable

from src.chess.chess import ChessPy
from src.chess.error import ChessError
from src.models.score import ScoreName

from ..models import Game, Puzzle, Color


class PuzzleCreator(Protocol):
    """
    Puzzle Creator Interface

    Puzzle creator implementations are responsible for creating
    chess puzzles based on some rules. Given game should be
    already analyzed before invoking any methods or
    creator will always return empty iterable.
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
        self.chessboard = ChessPy()

    def create(self, game: Game) -> list[Puzzle]:
        if game.analyses is None:
            return []

        puzzles: list[Puzzle] = []
        start = 10 if game.side == Color.WHITE else 11

        for i in range(start, len(game.moves) - 1, 2):
            move = game.moves[i]
            best_lines = game.analyses[i]
            best_score = best_lines[0].score
            next_best_score = game.analyses[i + 1][0].score

            if (
                next_best_score.score_name == ScoreName.CP
                and best_score.score_name == ScoreName.CP
                and (-400 < next_best_score.score_value < 400)
                and (
                    abs(next_best_score.score_value)
                    - abs(best_score.score_value)
                    > 100
                )
            ):
                uci_moves = [move.uci_move.value for move in game.moves[:i]]

                try:
                    self.chessboard.from_fen(game.initial_fen)
                    for uci_move in uci_moves:
                        self.chessboard.move(uci_move)
                    fen = self.chessboard.to_fen()
                except (ChessError, TypeError) as e:
                    return puzzles
                puzzles.append(
                    Puzzle(
                        fen=fen,
                        move=move,
                        score=next_best_score,
                        best_lines=best_lines,
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

    engine = LocalStockfishEngine("stockfish", depth=18, multipv=1, max_workers=10)
    analysis_parser = StockfishAnalysisParser()

    for game in games:
        uci_moves = [move.uci_move.value for move in game.moves]
        engine_result = await engine.analyze(game.initial_fen, uci_moves)
        analyses = []
        for i, analysis in enumerate(engine_result):
            best_lines = []
            for line in analysis:
                analysis = analysis_parser.parse(line, game.initial_fen, game.moves[:i])
                best_lines.append(analysis)
            analyses.append(best_lines)
        game.analyses = analyses

    for game in games:
        print("GAME: ", game, "\n\n")

    creator = AnalysisBasedPuzzleCreator()
    puzzles = [creator.create(game) for game in games]

    for puzzle in puzzles:
        print(puzzle, "\n\n")


if __name__ == "__main__":
    from asyncio import run

    run(main())

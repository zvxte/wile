from typing import Any

from .fetcher import ChessComFetcher
from .parser import ChessComGameParser, StockfishAnalysisParser
from .chess import ChessPy
from .engine.stockfish import LocalStockfishEngine
from .puzzle import AnalysisBasedPuzzleCreator
from .models import Game, Move, Analysis, Puzzle


async def example():
    USERNAME = "hikaru"
    SINCE = 1722902400
    UNTIL = 1722988800
    LIMIT = 3
    DEPTH = 18
    MULTIPV = 3  # How many best lines to return in a position
    MAX_WORKERS = 8  # How many chess engine instances to run at the same time

    # === Fetch games === #
    fetcher = ChessComFetcher()
    fetched_games: list[dict[str, Any]] = await fetcher.fetch(USERNAME, SINCE)

    game_parser = ChessComGameParser()
    games: list[Game] = [
        game_parser.parse(game, USERNAME) for game in fetched_games[:LIMIT]
    ]

    # === Analyze games === #
    engine = LocalStockfishEngine("stockfish", DEPTH, MULTIPV, MAX_WORKERS)
    analysis_parser = StockfishAnalysisParser()
    for game in games:
        analyses: list[list[Analysis]] = []
        uci_moves: list[str] = [move.uci_move.value for move in game.moves]

        # Outer list represents each move, inner list holds n best lines
        unparsed_analyses: list[list[str]] = await engine.analyze(
            game.initial_fen, uci_moves
        )

        analyses: list[list[Analysis]] = []
        for i, unparsed_best_lines in enumerate(unparsed_analyses):
            best_lines: list[Analysis] = []
            for line in unparsed_best_lines:
                best_lines.append(
                    analysis_parser.parse(line, game.initial_fen, game.moves[:i])
                )
            analyses.append(best_lines)
        game.analyses = analyses

    # === Create puzzles === #
    puzzle_creator = AnalysisBasedPuzzleCreator()
    puzzles: list[Puzzle] = []
    for game in games:
        puzzles.extend(puzzle_creator.create(game))

    print(f"Found {len(puzzles)} puzzles", end="\n\n")

    for puzzle in puzzles:
        print(puzzle, end="\n\n")


if __name__ == "__main__":
    from asyncio import run

    run(example())

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

    fetcher = ChessComFetcher()
    fetched_games: list[dict[str, Any]] = await fetcher.fetch(USERNAME, SINCE)

    game_parser = ChessComGameParser()
    games: list[Game] = [
        game_parser.parse(game, USERNAME) for game in fetched_games[:LIMIT]
    ]

    # Set UCI notations to be able to communicate with chess engine
    chessboard = ChessPy()
    for game in games:
        chessboard.from_fen(game.initial_fen)
        for move in game.moves:
            uci_move: str = chessboard.san_to_uci(move.san_move)
            chessboard.move(uci_move)
            move.uci_move = uci_move

    # Analyze game positions
    engine = LocalStockfishEngine("stockfish", DEPTH, MULTIPV, MAX_WORKERS)
    analysis_parser = StockfishAnalysisParser()
    for game in games:
        uci_moves: list[str] = []
        for move in game.moves:
            if move.uci_move is None:
                raise ValueError("uci_move should be set")
            uci_moves.append(move.uci_move)

        results: list[list[str]] = await engine.analyze(game.initial_fen, uci_moves)

        # Append each position analysis result to it's move
        for i in range(len(game.moves)):
            move: Move = game.moves[i]
            if move.side is None:
                raise ValueError("side should be set")
            best_lines: list[str] = results[i]

            # Parse engine's result
            analyses: list[Analysis] = []
            for line in best_lines:
                analyses.append(analysis_parser.parse(line, move.side))
            move.analyses = analyses

            # Update analysis score for the previous move
            if i > 1:
                previous_move = game.moves[i - 1]
                previous_move.score = analyses[0].score

    puzzle_creator = AnalysisBasedPuzzleCreator()
    puzzles: list[Puzzle] = []
    for game in games:
        puzzles += puzzle_creator.create(game)

    print(f"Found {len(puzzles)} puzzles")

    for puzzle in puzzles:
        print("---PUZZLE---\n", puzzle, "------------\n")


if __name__ == "__main__":
    from asyncio import run

    run(example())

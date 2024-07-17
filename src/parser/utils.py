from re import compile


# Regular expression pattern to get moves found in pgn
PGN_MOVES_PATTERN = compile(r"\d+\.+\s([a-hxNBRQKO1-8\-\+\#\=]+)")


def parse_pgn_moves(pgn: str) -> list[str]:
    return PGN_MOVES_PATTERN.findall(pgn)

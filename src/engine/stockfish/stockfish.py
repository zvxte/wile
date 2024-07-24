class LocalStockfishEngine:
    """
    Local Stockfish Engine
    
    Args:
        path (str): Path to Stockfish engine executable
        depth (int): Stockfish analysies depth
        max_workers (int): Number of Stockfish processes running at the same time

    Raises:
        AssertionError: If arguments with invalid types are provided.
    """

    def __init__(self, path: str, depth: int = 18, max_workers: int = 1):
        assert isinstance(path, str)
        assert isinstance(depth, int)
        assert isinstance(max_workers, int)

        self.path = path
        self.depth = depth
        self.max_workers = max_workers

    async def analyse(self, uci_moves: list[str]) -> list[str]:
        # Todo
        ...


# class RemoteStockfishEngine:
    # Todo
    # ...

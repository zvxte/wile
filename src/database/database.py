from typing import Protocol


class Database(Protocol):
    """
    Database Interface
    """

    async def connect(self) -> None:
        raise NotImplementedError

    async def create_tables(self) -> None:
        raise NotImplementedError

    async def disconnect(self) -> None:
        raise NotImplementedError

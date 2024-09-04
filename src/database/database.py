from typing import Protocol, Any


class DatabaseManager(Protocol):
    """
    Database Manager Interface

    Database manager implementations are responsible for managing
    database connections (opening and closing connections).
    Additionally, they handle the creation of tables, ensuring
    that the database is properly set up.
    """

    async def connect(self) -> None:
        """Connects to the database"""
        raise NotImplementedError

    async def disconnect(self) -> None:
        """Disconnects from the database"""
        raise NotImplementedError

    def connection(self) -> Any:
        """
        Returns:
            Any: Connection to the database. Type depends on a specific implementation.
        """
        raise NotImplementedError

    async def create_tables(self) -> None:
        """Creates tables"""
        raise NotImplementedError

"""
Repository Design Pattern

Repository implementations are responsible for
managing records in a database.
"""

from typing import Protocol


class UserRepository(Protocol):
    pass


class SessionRepository(Protocol):
    pass


class PlatformRepository(Protocol):
    pass


class GameRepository(Protocol):
    pass


class PuzzleRepository(Protocol):
    pass

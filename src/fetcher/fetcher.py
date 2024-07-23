from datetime import date
from time import time
from typing import Any, Iterable, Optional, Protocol

from httpx import AsyncClient, HTTPError

from .error import FetcherError


class Fetcher(Protocol):
    """Fetcher Interface"""

    async def fetch(
        self,
        username: str,
        since: int,
        until: Optional[int] = None,
    ) -> Iterable[Any]:
        """
        Fetches chess games

        Args:
            username (str): Username of a player.
            since (int): Since when to fetch the games as unix timestamp.
            until (int, optional): Until when to fetch the games as unix timestamp. Defaults to now.

        Returns:
            Iterable[Any]: All fetched games.

        Raises:
            AssertionError: If arguments with invalid types are provided.
            FetcherError: If arguments are logically invalid; If failed to fetch games.
        """
        raise NotImplementedError


class ChessComFetcher:
    async def fetch(
        self,
        username: str,
        since: int,
        until: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        # Fetching from Chess.com public API
        # https://www.chess.com/news/view/published-data-api

        current_timestamp = int(time())
        if until is None:
            until = current_timestamp

        assert isinstance(username, str), ["Invalid username type", username]
        assert isinstance(since, int), ["Invalid since type", since]
        assert isinstance(until, int), ["Invalid until type", until]

        if (
            len(username) < 3
            or since > current_timestamp
            or until > current_timestamp
            or since < 1177977600  # May 1, 2007
            or until < 1177977600
            or since > until
        ):
            raise FetcherError("Invalid arguments")

        since_date = date.fromtimestamp(since)
        until_date = date.fromtimestamp(until)

        urls: list[str] = []
        for year in range(since_date.year, until_date.year + 1):
            for month in range(1, 13):
                if year == since_date.year and month < since_date.month:
                    continue
                if year == until_date.year and month > until_date.month:
                    break
                urls.append(
                    f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02}"
                )

        games: list[dict[str, Any]] = []
        async with AsyncClient() as client:
            for url in urls:
                try:
                    response = await client.get(url)
                    games.extend(response.json()["games"])
                except HTTPError or KeyError as e:
                    raise FetcherError(e)
        try:
            return [
                game
                for game in games
                if since <= game["end_time"] <= until and game["rules"] == "chess"
            ]
        except KeyError as e:
            raise FetcherError(e)


async def main():
    # testing
    fetcher = ChessComFetcher()
    games = await fetcher.fetch("hikaru", 1720742400)  # since July 12, 2024
    for game in games:
        print(dumps(game, indent=4), end="\n\n")


if __name__ == "__main__":
    from asyncio import run
    from json import dumps

    run(main())

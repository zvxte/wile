from asyncio import run
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
        limit: Optional[int] = None,
    ) -> Iterable[Any]:
        """
        Fetches chess games

        Raises:
            FetcherError
        """
        raise NotImplementedError


class ChessComFetcher:
    async def fetch(
        self,
        username: str,
        since: int,
        until: Optional[int] = None,
        limit: Optional[int] = None,  # Unused in this implementation
    ) -> list[dict[str, Any]]:
        # Chess.com public API
        # https://www.chess.com/news/view/published-data-api

        current_timestamp = int(time())
        if until is None:
            until = current_timestamp
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
            return [game for game in games if since <= game["end_time"] <= until and game["rules"] == "chess"]
        except KeyError as e:
            raise FetcherError(e)


async def main():
    # testing
    fetcher = ChessComFetcher()
    games = await fetcher.fetch("hikaru", 1720742400)  # July 12, 2024
    for game in games:
        print(game, "\n\n\n")


if __name__ == "__main__":
    run(main())

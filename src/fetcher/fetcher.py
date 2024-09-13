from datetime import date
from time import time
from typing import Any, Iterable, Protocol
from json import loads

from httpx import AsyncClient, HTTPError

from .error import FetcherError


class Fetcher(Protocol):
    """
    Fetcher Interface

    Fetcher implementations are responsible for fetching games from
    various chess platforms. Fetched games should be later on parsed
    using appropriate game parser.
    """

    async def fetch(
        self,
        username: str,
        since: int,
        until: int | None = None,
    ) -> Iterable[Any]:
        """
        Fetches chess games

        Args:
            username (str)
            since (int): Since when to fetch the games as unix timestamp.
            until (int | None): Until when to fetch the games as unix timestamp. Defaults to now.

        Returns:
            Iterable[Any]: All found games. Iterable could be empty if no game was found.

        Raises:
            TypeError
            ValueError
            FetcherError: If arguments are logically invalid. If failed to fetch games.
        """
        raise NotImplementedError


class ChessComFetcher:
    async def fetch(
        self,
        username: str,
        since: int,
        until: int | None = None,
    ) -> list[dict[str, Any]]:
        # Fetching from Chess.com public API
        # https://www.chess.com/news/view/published-data-api
        # Endpoint:
        # https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}

        current_timestamp = int(time())
        if until is None:
            until = current_timestamp
        elif until > current_timestamp:
            until = current_timestamp

        if (
            not isinstance(username, str)
            or not isinstance(since, int)
            or not isinstance(until, int)
        ):
            raise TypeError("Invalid argument types")

        if (
            len(username) < 3
            or since > current_timestamp
            or since < 1177977600  # May 1, 2007
            or until < 1177977600
            or since > until
        ):
            raise ValueError("Invalid argument values")

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
            # Send requests synchronously to not encounter any rate limiting
            for url in urls:
                try:
                    response = await client.get(url)
                    games.extend(response.json()["games"])
                except (HTTPError, KeyError) as e:
                    raise FetcherError(e)
        try:
            return [
                game
                for game in games
                if since <= game["end_time"] <= until and game["rules"] == "chess"
            ]
        except KeyError as e:
            raise FetcherError(e)


class LichessFetcher:
    async def fetch(
        self,
        username: str,
        since: int,
        until: int | None = None,
    ) -> list[dict[str, Any]]:
        # Fetching from Lichess.org public API
        # https://lichess.org/api#tag/Games/operation/apiGamesUser
        # Endpoint:
        # https://lichess.org/api/games/user/{username} + query parameters

        current_timestamp = int(time())
        if until is None:
            until = current_timestamp
        elif until > current_timestamp:
            until = current_timestamp

        if (
            not isinstance(username, str)
            or not isinstance(since, int)
            or not isinstance(until, int)
        ):
            raise TypeError("Invalid argument types")

        if (
            len(username) < 2
            or since > current_timestamp
            or since < 1356998400  # Jan 1, 2013
            or until < 1356998400
            or since > until
        ):
            raise ValueError("Invalid argument values")

        url = f"https://lichess.org/api/games/user/{username}"
        headers = {
            "Accept": "application/x-ndjson",
        }
        params = {
            "since": since * 1000,
            "until": until * 1000,
            "perfType": "ultraBullet,bullet,blitz,rapid,classical,correspondence,chess960",
        }

        games = []
        async with AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, params=params)
                for game in response.iter_lines():
                    games.append(loads(game))
            except HTTPError as e:
                raise FetcherError(e)

        return games


async def main():
    # testing
    # chesscom_fetcher = ChessComFetcher()
    # games = await chesscom_fetcher.fetch("hikaru", 1720742400)  # since July 12, 2024
    # for game in games:
    #     print(dumps(game, indent=4), end="\n\n")

    lichess_fetcher = LichessFetcher()
    games = await lichess_fetcher.fetch("", 1723208004, 1723380804)
    for game in games:
        print(game, "\n\n")


if __name__ == "__main__":
    from asyncio import run
    from json import dumps

    run(main())

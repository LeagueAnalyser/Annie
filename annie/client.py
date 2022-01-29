from collections.abc import Coroutine
from typing import Any
from urllib.parse import urljoin
import aiohttp
import pydantic

from .objects import Summoner


class Client:
    def __init__(self, token: str) -> None:
        self.base = 'https://{root}.api.riotgames.com'
        self.headers = {
            'X-Riot-Token': token,
            'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.session = aiohttp.ClientSession()
        self.max_retries = 5

    async def get(self, endpoint: str, root: str = 'euw') -> Coroutine[Any, Any, Any]:
        url = urljoin(self.base, endpoint)
        retry = 0
        while retry < self.max_retries:
            async with self.session.get(url.format(root)) as response:
                if (300 < response.status < 200):
                    retry += 1
                    continue
                return response.json()
        raise ValueError('max retires exceeded in call')

    async def get_summoner_by_name(self, name: str, root: str) -> None: ...
    async def get_summoner_by_summoner_id(self, summoner_id: str, root: str) -> None: ...
    async def get_league_by_summoner(self, summoner: Summoner | str, root: str) -> None: ...
    async def get_champion_rotation(self) -> None: ...
    async def get_mastery_by_summoner(self, summoner: Summoner | str, root: str) -> None: ...

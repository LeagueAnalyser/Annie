import aiohttp

from .objects import Summoner


# _by_summoner methods should accept either a summoner: str (summoner Id)
# or a summoner: Summoner (Summoner object)


class Client:
    def __init__(self, token: str) -> None:
        self.base = 'https://{root}.api.riotgames.com'
        self.headers = {
            'X-Riot-Token': token,
            'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.session = aiohttp.ClientSession()

    def get_summoner_by_name(self, name: str) -> None: ...
    def get_summoner_by_summoner_id(self, summoner_id: str) -> None: ...
    def get_league_by_summoner(self, summoner: Summoner | str) -> None: ...
    def get_champion_rotation(self) -> None: ...
    def get_mastery_by_summoner(self, summoner: Summoner | str) -> None: ...

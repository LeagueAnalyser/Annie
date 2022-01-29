import requests
import pydantic
import json
import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40",
    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-0e91a351-28f1-4c67-b068-8ee8626ce2af"
}

class SummonerBySummonerName(pydantic.BaseModel):
    """ Get a summonder by summoner name
        /lol/summoner/v4/summoners/by-name/{summonerName}
    """
    id: str # encrypted summoner id
    accountId: str # encrypted account id
    puuid: str # encrypted PUUID
    name: str
    revisionDate: datetime.datetime
    profileIconId: int
    summonerLevel: int

class TotalMasteryScore(pydantic.BaseModel):
    """ Get total mastery score (sum of individual champ. mastery levels)
    /lol/champion-mastery/v4/scores/by-summoner/{encryptedSummonerId}
    """
    score: int

class MasteryByChamp(pydantic.BaseModel):
    """ Get all chamption mastery entries sorted by number of champ. points decending
        /lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}
    """
    championId: int
    championLevel: int
    championPoints: int
    lastPlayTime: int
    championPointsSinceLastLevel: int
    championPointsUntilNextLevel: int
    chestGranted: bool
    tokensEarned: int
    summonerId: str

class ChallengerPlayer(pydantic.BaseModel):
    """ Get the challenger league of given queue 
        (RANKED_SOLO_5x5, RANKED_FLEX_SR)
        /lol/league/v4/challengerleagues/by-queue/{queue}
    """
    summonerId : str
    summonerName: str
    leaguePoints: int
    rank: str
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    freshBlood: bool
    hotStreak: bool


if __name__ == '__main__':

    # SummonerBySummonerName
    zak = requests.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Redditmod", headers=headers).json()
    zak_object = pydantic.parse_obj_as(SummonerBySummonerName, zak)

    # TotalMasteryScore
    zak_mastery = requests.get("https://euw1.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/"+zak_object.id, headers=headers).json()
    zak_mastery_object = TotalMasteryScore(score=zak_mastery)

    # MasteryByChamp
    zak_mastery_by_champ = requests.get("https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+zak_object.id, headers=headers).json()
    zak_mastery_by_champ_object =  pydantic.parse_obj_as(list[MasteryByChamp], zak_mastery_by_champ)

    # ChallengerLeague
    challenger = (requests.get("https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5", headers=headers).json())["entries"]
    challenger_object = pydantic.parse_obj_as(list[ChallengerPlayer], challenger)


__author__ = 'cmayer'

from BaseModel import BaseModel
from Player import Player
from LeagueConsts import LeagueConsts
from League import League
from Stats import Stats


class DBController(BaseModel):

    def checkInit(self, leagueFile):
        #if player table does not exist, create it
        Stats.create_table(True)
        Player.create_table(True)
        League.create_table(True)
        LeagueConsts.initLeague(leagueFile)

    @staticmethod
    def getLeagueConsts():
        return LeagueConsts()
__author__ = 'cmayer'


from Player import Player
from LeagueConsts import LeagueConsts
from League import League
from Stats import Stats


class DBController():

    def checkInit(self):
        #if player table does not exist, create it
#        Stats.create_table(True)
        Player.create_table(True)
        League.create_table(True)

    @staticmethod
    def getLeagueConsts():
        return LeagueConsts()
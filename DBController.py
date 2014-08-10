__author__ = 'cmayer'

from BaseModel import BaseModel
from Player import Player
from LeagueConsts import LeagueConsts
from League import League


class DBController(BaseModel):

    def checkInit(self):
        #if player table does not exist, create it
        Player.create_table(True)
        League.create_table(True)

    @staticmethod
    def findPlayerByName(name):
        modName = name.replace("-","0")
        retval = Player.select().where(Player.Name == modName).first()
        return retval

    @staticmethod
    def findPlayer(name, dob):
        retval = Player.select().where((Player.Name == name) & (Player.DOB == dob)).first()
        return retval

    @staticmethod
    def getLeagueConsts():
        return LeagueConsts()
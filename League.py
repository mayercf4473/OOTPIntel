__author__ = 'cmayer'

from BaseModel import BaseModel
from peewee import *
import json

class League():
    franchiseMap = dict()

    class Team(BaseModel):
        team = CharField(index=True, max_length=8)
        level = CharField(index=True, max_length=8)
        franchise = CharField()

    @staticmethod
    def create_table(unused):
        League.Team.create_table(True)

    def loadTeams(self, jsonFileName):
        f = open(jsonFileName, "r")
        jsonObj = json.load(f)
        for teamBlock in jsonObj['Teams']:
            team = self.Team()
            team.team = teamBlock['Team']
            team.level = 'ML'
            team.franchise = team.team
            for minorTeam in teamBlock['minors']:
                mteam = self.Team()
                mteam.team = minorTeam['Team']
                mteam.level = minorTeam['Level']
                mteam.franchise = team.team
                mteam.save()
            team.save()

    @staticmethod
    def findFranchise(team, level):
        #TODO re-write by having select return a list, and check length
        count = 0;
        retval = ""
        for uteam in League.Team.select().where((League.Team.team == team) & (League.Team.level == level)):
            retval = uteam.franchise
            count += 1
        if count > 1:
            raise NameError('Multiple teams found for ' + team + ':' + level)
            print "HACK setting " + team + " to SEA"
            retval = "SEA"
        return retval

#TODO problem with duplicate teams.



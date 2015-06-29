__author__ = 'cmayer'

from BaseModel import BaseModel
from peewee import *
import json

class League():
    franchiseMap = dict()
    minRating = 0
    maxRating = 0
    minPotential = 0
    maxPotential = 0

    class Team(BaseModel):
        team = CharField(index=True, max_length=8)
        fullTeam = CharField(max_length=32)
        level = CharField(index=True, max_length=8)
        franchise = CharField()

    @staticmethod
    def create_table(unused):
        League.Team.create_table(True)

    def loadTeams(self, jsonFileName):
        f = open(jsonFileName, "r")
        jsonObj = json.load(f)

        self.minRating = int(jsonObj['MinR'])
        self.maxRating = int(jsonObj['MaxR'])
        self.minPotential = int(jsonObj['MinP'])
        self.maxPotential = int(jsonObj['MaxP'])

        for teamBlock in jsonObj['Teams']:
            team = self.Team()
            team.team = teamBlock['Team']
            team.level = 'ML'
            team.franchise = team.team
            team.fullTeam = ""
            for minorTeam in teamBlock['minors']:
                mteam = self.Team()
                mteam.team = minorTeam['Team']
                mteam.level = minorTeam['Level']
                if 'FullTeam' in minorTeam:
                    mteam.fullTeam = minorTeam['FullTeam']
                else:
                    mteam.fullTeam = ""
                mteam.franchise = team.team
                mteam.save()
            team.save()

    @staticmethod
    def findFranchise(team, level, fullTeam):
        if level == "INT":
            return team

        count = 0;
        retval = ""
        useFullTeam = False
        found = False
        selectList = League.Team.select().where((League.Team.team == team) & (League.Team.level == level))
        if selectList.count() > 1:
            useFullTeam = True
        for uteam in selectList:
            if not useFullTeam or uteam.fullTeam == fullTeam:
                retval = uteam.franchise
                found = True

        if (not found):
            if not level == "INT":
                print "No Franchise for " + team + level + fullTeam

        return retval



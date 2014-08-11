__author__ = 'cmayer'

#from BaseModel import BaseModel
#from peewee import *

from BaseModel import BaseModel
from peewee import *
from League import League

class ConstGroup:
    minRating = 0
    maxRating = 0
    deltaMinMax = maxRating - minRating
    battingCo = 19
    pitchingCo = 249
    speedCo = 249
    fieldCo = 99
    stealingCo = 99


class LeagueConsts():
    normal = ConstGroup()
    potential = ConstGroup()

    class LeagueConstDB(BaseModel):
        minRating = IntegerField(default=20)
        maxRating = IntegerField(default=80)
        minRatingP = IntegerField(default=20)
        maxRatingP = IntegerField(default=80)

    @staticmethod
    def initLeague(leagueFile):
        LeagueConsts.LeagueConstDB.create_table(True)
        if LeagueConsts.LeagueConstDB.select().count() == 0:
            lg = LeagueConsts.LeagueConstDB()
            league = League()
            league.loadTeams(leagueFile)
            lg.minRating = league.minRating
            lg.maxRating = league.maxRating
            lg.minRatingP = league.minPotential
            lg.maxRatingP = league.maxPotential
            lg.save()

    def __init__(self):
        if self.normal.minRating == 0:
            dbconsts = self.LeagueConstDB.select().first()
            self.normal.minRating = dbconsts.minRating
            self.normal.maxRating = dbconsts.maxRating
            self.potential.minRating = dbconsts.minRatingP
            self.potential.maxRating = dbconsts.maxRatingP
        self.normal.deltaMinMax = self.normal.maxRating - self.normal.minRating
        self.potential.deltaMinMax = self.potential.maxRating - self.potential.minRating





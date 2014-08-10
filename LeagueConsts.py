__author__ = 'cmayer'

#from BaseModel import BaseModel
#from peewee import *

from BaseModel import BaseModel
from peewee import *

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
    def initLeague(min, max, minP, maxP):
        LeagueConsts.LeagueConstDB.create_table(True)
        if LeagueConsts.LeagueConstDB.select().count() == 0:
            lg = LeagueConsts.LeagueConstDB()
            lg.minRating = min
            lg.maxRating = max
            lg.minRatingP = minP
            lg.maxRatingP = maxP
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





__author__ = 'cmayer'

from BaseModel import BaseModel
from peewee import *
from LeagueConsts import LeagueConsts
from League import League
from Player import Player
import BaseballFunctions

#This is a row of the player table, that contains all ratings information about a player
#In the future we may place some stats here as well to refine the prediction model for future performance
class Stats(BaseModel):
    #stats include FirstName, LastName, BirthDay (this tuple should be unique)
    #Team, Bats(L,R,S), Throws(L,R)...
    PlayerId = ForeignKeyField(Player)
    Position = CharField()
    Year = IntegerField()
    Name = CharField(index=True, max_length=64)
    DOB = CharField(index=True, max_length=64)
    AB = IntegerField()
    IP = FloatField()
    wOBA = FloatField()
    wRAA = FloatField()
    FIP = FloatField()
    pWAR = FloatField()
    wSB = FloatField()
    UZR = FloatField()
    bWAR = FloatField()

    def initFromString(self, year, dataString, headerDict):
        fieldArray = dataString.split(',')
        self.Position = fieldArray[headerDict['POS']]
        self.Name = unicode(fieldArray[headerDict['Name']], errors="ignore")
        self.DOB = fieldArray[headerDict['DOB']]

        player = Player.findPlayer(self.Name, self.DOB)
        if not player:
            print ("No Player found for " + self.Name + self.DOB)

        self.PlayerId = player

        self.Year = year

        self.AB = int(fieldArray[headerDict['AB']])
        hits = int(fieldArray[headerDict['H']])
        doubles = int(fieldArray[headerDict['2B']])
        triples = int(fieldArray[headerDict['3B']])
        homeRuns = int(fieldArray[headerDict['HR']])
        walks = int(fieldArray[headerDict['BB']])
        self.IP = float(fieldArray[headerDict['IP']])

        strikeouts = int(fieldArray[headerDict['K']])
        homeRunsAgainst  = int(fieldArray[headerDict['HRa']])
        walksAgainst = int(fieldArray[headerDict['BBa']])

        sb = int(fieldArray[headerDict['SB']])
        cs = int(fieldArray[headerDict['CS']])
        self.UZR = float(fieldArray[headerDict['ZR']])

        singles = hits - doubles - triples - homeRuns
        self.wOBA = BaseballFunctions.rawWOBA(self.AB, walks, singles, doubles, triples, homeRuns)
        self.wRAA = BaseballFunctions.rawWRAA(self.AB, self.wOBA, walks)
        self.FIP = BaseballFunctions.rawFIP(self.IP, strikeouts, homeRunsAgainst, walksAgainst)

        self.wSB = BaseballFunctions.rawWSB(sb, cs)

        self.bWAR = (self.wRAA + self.wSB + self.UZR)/10
        self.pWAR = BaseballFunctions.rawPWAR(self.IP, self.FIP)

        class Meta:
            order_by = ('Name',)



    @staticmethod
    def findPlayer(name, dob, year):
        retval = Stats.select().where((Stats.Name == name) & (Stats.DOB == dob) & (Stats.Year == year)).first()
        return retval

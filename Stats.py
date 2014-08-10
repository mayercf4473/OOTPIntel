__author__ = 'cmayer'

from BaseModel import BaseModel
from peewee import *
from LeagueConsts import LeagueConsts
from League import League


#This is a row of the player table, that contains all ratings information about a player
#In the future we may place some stats here as well to refine the prediction model for future performance
class Stats(BaseModel):
    #stats include FirstName, LastName, BirthDay (this tuple should be unique)
    #Team, Bats(L,R,S), Throws(L,R)...
    Position = CharField()
    Name = CharField(index=True, max_length=64)
    DOB = CharField(index=True, max_length=64)
    wOBA = FloatField()
    wRAA = FloatField()
    FIP = FloatField()
    pWAR = FloatField()
    wSB = FloatField()
    UZR = FloatField()
    bWAR = FloatField()

    def initFromString(self, year, dataString, headerDict):
        dataString = dataString.replace('-','0')
        fieldArray = dataString.split(',')
        self.Position = fieldArray[headerDict['POS']]
        self.Name = unicode(fieldArray[headerDict['Name']], errors="ignore")
        self.DOB = fieldArray[headerDict['DOB']]

        hits = fieldArray[headerDict['Hits']]
        doubles = fieldArray[headerDict['Doubles']]
        triples = fieldArray[headerDict['Triples']]
        homeRuns = fieldArray[headerDict['HR']]
        walks = fieldArray[headerDict['BB']]

        strikeouts = fieldArray[headerDict['K']]
        homeRunsAgainst  = fieldArray[headerDict['HRA']]
        walksAgainst = fieldArray[headerDict['BBa']]

        sb = fieldArray[headerDict['SB']]
        sba = fieldArray[headerDict['SBA']]
        self.UZR = fieldArray[headerDict['ZR']]

        singles = hits - doubles - triples - homeRuns
        self.wOBA = Stats.rawWOBA(walks, singles, doubles, triples, homeRuns)
        self.wRAA = Stats.rawWRAA(self.wOBA, walks)
        self.FIP = Stats.rawFIP(strikeouts, homeRunsAgainst, walksAgainst)

        self.wSB = Stats.rawWSB()

        self.bWAR = (self.wRAA + self.wSB + self.UZR)/10
        self.pWAR = Stats.calcPWAR(self.FIP)

        class Meta:
            order_by = ('Name',)

    @staticmethod
    def rawWOBA(walks, singles, doubles, triples, homeRuns):
        #assumes above calculations are for 1000 at bats
        wOBA = (walks * .72 + singles * .9 + doubles * 1.24 + triples * 1.56 + homeRuns * 1.95) / (1000 + walks)
        return wOBA

    @staticmethod
    def rawWRAA(woba, walks):
        #=(1000+AF2)*(AP2-320)/1200
        return (1000+walks) * (woba - .320) / 1.2

    @staticmethod
    def rawFIP(strikeOuts, homeRuns, walks):
        return (13*homeRuns + 3*walks - 2*strikeOuts)/136 + 3.2

    #very rough wSB
    @staticmethod
    def rawWSB(sb, sba):
        return sb * .2 + (sba - sb) * .32

    @staticmethod
    def rawPWAR(pos, fip):
          #250 IP for starter, 80 for others.  multiply by 10/6 to brings to 1000AB scale
        base = 80
        if pos == "SP":
            base = 250
        innings = base * 10/6
        lgFIP = 4.28
        return (lgFIP - fip) / 9 * innings / 10




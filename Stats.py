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
        self.wOBA = Stats.rawWOBA(self.AB, walks, singles, doubles, triples, homeRuns)
        self.wRAA = Stats.rawWRAA(self.AB, self.wOBA, walks)
        self.FIP = Stats.rawFIP(self.IP, strikeouts, homeRunsAgainst, walksAgainst)

        self.wSB = Stats.rawWSB(sb, cs)

        self.bWAR = (self.wRAA + self.wSB + self.UZR)/10
        self.pWAR = Stats.rawPWAR(self.IP, self.FIP)

        class Meta:
            order_by = ('Name',)

    @staticmethod
    def rawWOBA(ab, walks, singles, doubles, triples, homeRuns):
        #assumes above calculations are for 1000 at bats
        if (ab + walks) <= 0:
            wOBA = 0
        else:
            wOBA = (walks * .72 + singles * .9 + doubles * 1.24 + triples * 1.56 + homeRuns * 1.95) / (ab + walks)
        return wOBA

    @staticmethod
    def rawWRAA(ab, woba, walks):
        #=(1000+AF2)*(AP2-320)/1200
        return (ab+walks) * (woba - .320) / 1.2

    @staticmethod
    def rawFIP(ip, strikeOuts, homeRuns, walks):
        if ip <= 0:
            return 99
        return (13*homeRuns + 3*walks - 2*strikeOuts)/ip + 3.2

    #very rough wSB
    @staticmethod
    def rawWSB(sb, cs):
        return sb * .2 + cs * .32

    @staticmethod
    def rawPWAR(innings, fip):
        if innings <= 0:
            return -20
        lgFIP = 4.28
        return (lgFIP - fip) / 9 * innings / 10


    @staticmethod
    def findPlayer(name, dob, year):
        retval = Stats.select().where((Stats.Name == name) & (Stats.DOB == dob) & (Stats.Year == year)).first()
        return retval

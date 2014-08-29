import math

__author__ = 'cmayer'

from BaseModel import BaseModel
from peewee import *
from LeagueConsts import LeagueConsts
from League import League
import BaseballFunctions

constAB=550
constIP=230

#This is a row of the player table, that contains all ratings information about a player
#In the future we may place some stats here as well to refine the prediction model for future performance
class Player(BaseModel):
    class Meta:
        db_name = "upcoming"

    #stats include FirstName, LastName, BirthDay (this tuple should be unique)
    #Team, Bats(L,R,S), Throws(L,R)...
    Position = CharField()
    Name = CharField(index=True, max_length=64)
    Team = CharField()
    Level = CharField()
    DOB = CharField(index=True, max_length=64)
    Age = IntegerField()
    Bats = CharField()
    Throws = CharField()
    Overall = IntegerField()
    Potential = IntegerField()
    Leadership = IntegerField()
    WorkEthic = IntegerField()
    Intelligence = IntegerField()
    CON = IntegerField()
    GAP = IntegerField()
    POW = IntegerField()
    EYE = IntegerField()
    Ks = IntegerField()
    CONvL = IntegerField()
    GAPvL = IntegerField()
    POWvL = IntegerField()
    EYEvL = IntegerField()
    KvL = IntegerField()
    CONvR = IntegerField()
    GAPvR = IntegerField()
    POWvR = IntegerField()
    EYEvR = IntegerField()
    KvR = IntegerField()
    CONP = IntegerField()
    GAPP = IntegerField()
    POWP = IntegerField()
    EYEP = IntegerField()
    KP = IntegerField()
    STU = IntegerField()
    MOV = IntegerField()
    CONT = IntegerField()
    STUvL = IntegerField()
    MOVvL = IntegerField()
    CONTvL = IntegerField()
    STUvR = IntegerField()
    MOVvR = IntegerField()
    CONTvR = IntegerField()
    STUP = IntegerField()
    MOVP = IntegerField()
    CONTP = IntegerField()
    STM = IntegerField()
    GF = CharField()
    IFRNG = IntegerField()
    IFARM = IntegerField()
    TDP = IntegerField()
    IFERR = IntegerField()
    OFRNG = IntegerField()
    OFARM = IntegerField()
    OFERR = IntegerField()
    CARM = IntegerField()
    CABI = IntegerField()
    P = IntegerField()
    C = IntegerField()
    B1 = IntegerField()
    B2 = IntegerField()
    B3 = IntegerField()
    SS = IntegerField()
    LF = IntegerField()
    CF = IntegerField()
    RF = IntegerField()
    SPE = IntegerField()
    STE = IntegerField()
    RUN = IntegerField()
    wOBA = FloatField()
    wOBAvL = FloatField()
    wOBAvR = FloatField()
    wRAA = FloatField()
    wOBAP = FloatField()
    FIP = FloatField()
    FIPvL = FloatField()
    FIPvR = FloatField()
    FIPP = FloatField()
    pWAR = FloatField()
    pWARP = FloatField()
    wSB = FloatField()
    UZR = FloatField()
    UZRP = FloatField()
    bWAR = FloatField()
    bWARP = FloatField()
    CP = FloatField()
    B1P = FloatField()
    B2P = FloatField()
    B3P = FloatField()
    SSP = FloatField()
    CFP = FloatField()
    RFP = FloatField()
    LFP = FloatField()
    drafted = IntegerField(default=0)
    franchise = CharField(default='')

    def initFromString(self, dataString, headerDict, constants):
        dataString = dataString.replace('-','0')
        fieldArray = dataString.split(',')
        self.Position = fieldArray[headerDict['POS']]
        theName = unicode(fieldArray[headerDict['Name']], errors="ignore")
        self.Name = theName.replace('0','-')
        self.Team = unicode(fieldArray[headerDict['TMa']], errors="ignore").encode("ascii", "ignore")
        self.Level = fieldArray[headerDict['Lev']]
        self.DOB = fieldArray[headerDict['DOB']]
        self.Age=fieldArray[headerDict['Age']]
        self.Bats = fieldArray[headerDict['B']]
        self.Throws = fieldArray[headerDict['T']]
        self.Overall = fieldArray[headerDict['OVR']].split()[0]
        self.Potential = fieldArray[headerDict['POT']].split()[0]
        self.Leadership = self.personalityToNumber(fieldArray[headerDict['LEA']])
        self.WorkEthic = self.personalityToNumber(fieldArray[headerDict['WE']])
        self.Intelligence = self.personalityToNumber(fieldArray[headerDict['INT']])
        self.CON = int(fieldArray[headerDict['CON']])
        self.GAP = int(fieldArray[headerDict['GAP']])
        self.POW = int(fieldArray[headerDict['POW']])
        self.EYE = int(fieldArray[headerDict['EYE']])
        self.Ks = int(fieldArray[headerDict['Ks']])
        self.CONvL = fieldArray[headerDict['CON vL']]
        self.GAPvL = fieldArray[headerDict['GAP vL']]
        self.POWvL = fieldArray[headerDict['POW vL']]
        self.EYEvL = fieldArray[headerDict['EYE vL']]
        self.KvL = fieldArray[headerDict['K vL']]
        self.CONvR = fieldArray[headerDict['CON vR']]
        self.GAPvR = fieldArray[headerDict['GAP vR']]
        self.POWvR = fieldArray[headerDict['POW vR']]
        self.EYEvR = fieldArray[headerDict['EYE vR']]
        self.KvR = fieldArray[headerDict['K vR']]
        self.CONP = fieldArray[headerDict['CON P']]
        self.GAPP = fieldArray[headerDict['GAP P']]
        self.POWP = fieldArray[headerDict['POW P']]
        self.EYEP = fieldArray[headerDict['EYE P']]
        self.KP = fieldArray[headerDict['K P']]
        self.STU = fieldArray[headerDict['STU']]
        self.MOV = fieldArray[headerDict['MOV']]
        self.CONT = fieldArray[headerDict['CONa']]
        self.STUvL = fieldArray[headerDict['STU vL']]
        self.MOVvL = fieldArray[headerDict['MOV vL']]
        self.CONTvL = fieldArray[headerDict['CON vLa']]
        self.STUvR = fieldArray[headerDict['STU vR']]
        self.MOVvR = fieldArray[headerDict['MOV vR']]
        self.CONTvR = fieldArray[headerDict['CON vRa']]
        self.STUP = fieldArray[headerDict['STU P']]
        self.MOVP = fieldArray[headerDict['MOV P']]
        self.CONTP = fieldArray[headerDict['CON Pa']]
        self.STM = fieldArray[headerDict['STM']]
        self.GF = fieldArray[headerDict['G/F']]
        self.IFRNG = fieldArray[headerDict['IF RNG']]
        self.IFARM = fieldArray[headerDict['IF ARM']]
        self.TDP = fieldArray[headerDict['TDP']]
        self.IFERR = fieldArray[headerDict['IF ERR']]
        self.OFRNG = fieldArray[headerDict['OF RNG']]
        self.OFARM = fieldArray[headerDict['OF ARM']]
        self.OFERR = fieldArray[headerDict['OF ERR']]
        self.CARM = fieldArray[headerDict['C ARM']]
        self.CABI = fieldArray[headerDict['C ABI']]
        self.P = fieldArray[headerDict['P']]
        self.C = fieldArray[headerDict['C']]
        self.B1 = fieldArray[headerDict['1B']]
        self.B2 = fieldArray[headerDict['2B']]
        self.B3 = fieldArray[headerDict['3B']]
        self.SS = fieldArray[headerDict['SS']]
        self.LF = fieldArray[headerDict['LF']]
        self.CF = fieldArray[headerDict['CF']]
        self.RF = fieldArray[headerDict['RF']]
        self.SPE = int(fieldArray[headerDict['SPE']])
        self.STE = fieldArray[headerDict['STE']]
        self.RUN = fieldArray[headerDict['RUN']]

        self.calcStats(constants)

        fullTeam = unicode(fieldArray[headerDict['TM']], errors="ignore").encode("ascii", "ignore")

        if (self.Team and self.Team != '0' and self.Level):
            franchise = League.findFranchise(self.Team, self.Level, fullTeam)
            if franchise:
                self.franchise = franchise
            else:
                print "missing franchse: " + self.Team + "," + self.Level
        else:
            pass
            #print "bad data for " + self.Name

    def calcStats(self, constants):
        #250 IP for starter, 80 for others.
        base = 80
        if self.Position == "SP":
            base = 250
        innings = base

        self.wOBA = self.calcWOBA(self.CON, self.GAP, self.POW, self.EYE, self.Ks, self.SPE, constants.normal)
        self.wRAA = self.calcWRAA(self.wOBA, self.EYE, constants.normal)
        self.FIP = self.calcFIP(self.STU, self.MOV, self.CONT, constants.normal)
        self.wSB = self.calcwSB(constants.normal)
        self.calcUZR(constants.normal)
        self.calcUZRP(constants.normal)
        self.wOBAvL = self.calcWOBA(self.CONvL, self.GAPvL, self.POWvL, self.EYEvL, self.KvL, self.SPE, constants.normal)
        self.wOBAvR = self.calcWOBA(self.CONvR, self.GAPvR, self.POWvR, self.EYEvR, self.KvR, self.SPE, constants.normal)
        self.wOBAP = self.calcWOBA(self.CONP, self.GAPP, self.POWP, self.EYEP, self.KP, self.SPE, constants.potential)
        self.wRAAP = self.calcWRAA(self.wOBAP, self.EYEP, constants.potential)
        self.FIPP = self.calcFIP(self.STUP, self.MOVP, self.CONTP, constants.potential)
        self.FIPvL = self.calcFIP(self.STUvL, self.MOVvL, self.CONTvL, constants.normal)
        self.FIPvR = self.calcFIP(self.STUvR, self.MOVvR, self.CONTvR, constants.normal)

        self.bWAR = (self.wRAA + self.wSB + self.UZR)/10
        self.pWAR = BaseballFunctions.rawPWAR(innings, self.FIP)

        self.bWARP = (self.wRAAP + self.wSB + self.UZRP)/10
        self.pWARP = BaseballFunctions.rawPWAR(innings, self.FIPP)


        class Meta:
            order_by = ('Name',)

    def personalityToNumber(self, value):
        if value == "Very Low":
            return 0
        elif value == "Low":
            return 1
        elif value == "High":
            return 3
        elif value == "Very High":
            return 4
        return 2

    def calcWOBA(self, con, gap, pow, eye, ks, speed, consts):
        nCon = ((float(con) - consts.minRating)/consts.deltaMinMax) * consts.battingCo + 1
        nGap = ((float(gap) - consts.minRating)/consts.deltaMinMax) * consts.battingCo + 1
        nPow = ((float(pow) - consts.minRating)/consts.deltaMinMax) * consts.battingCo + 1
        nKs = ((float(ks) - consts.minRating)/consts.deltaMinMax) * consts.battingCo + 1
        nSpeed = ((float(speed) - consts.minRating) / consts.deltaMinMax) * consts.speedCo + 1

        hits = -0.0015*nCon*nCon + 1.1119*nCon + 42.642

        xbh = 0.2855 * nGap - 1.0371

        triples = 0
        if nSpeed < 50:
            triples = xbh * .03
        elif nSpeed < 90:
            triples = xbh * .06
        elif nSpeed < 130:
            triples = xbh * .11
        elif nSpeed < 180:
            triples = xbh * .14
        elif nSpeed < 200:
            triples = xbh * .17
        else:
            triples = xbh * .3

        doubles = xbh - triples

        homeRuns = 0.0008 * nPow * nPow + 0.0786*nPow + 1.4208


        singles = hits - doubles - triples - homeRuns

        walks = self.getWalks(eye, consts)

        return BaseballFunctions.rawWOBA(constAB, walks, singles, doubles, triples, homeRuns)

    def getWalks(self, eye, consts):
        nEye = ((float(eye) - consts.minRating)/consts.deltaMinMax) * consts.battingCo + 1
        walks = 0.0016* nEye * nEye + 0.4172*nEye - 0.9167

        return walks

    def calcWRAA(self, woba, eye, consts):
        #=(1000+AF2)*(AP2-320)/1200
        walks = self.getWalks(eye, consts)
        return BaseballFunctions.rawWRAA(constAB, woba, walks)

    def calcFIP(self, stuff, movement, control, consts):
        nControl = ((float(control) - consts.minRating)/consts.deltaMinMax) * consts.pitchingCo + 1
        nStuff = ((float(stuff) - consts.minRating)/consts.deltaMinMax) * consts.pitchingCo + 1
        nMovement = ((float(movement) - consts.minRating)/consts.deltaMinMax) * consts.pitchingCo + 1

        strikeOuts = 0.8936 * nStuff + 8.9379
        homeRuns = max(10, -0.1355 * nMovement + 43.86)
        walks = max(8, 0.0041 * nControl * nControl - 2.0004 * nControl + 250.9)

        return BaseballFunctions.rawFIP(constIP, strikeOuts, homeRuns, walks)

    def calcUZR(self, consts):
        ssUZR = (((float(self.SS) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.365 - 22.4
        b1UZR = (((float(self.B1) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.167 - 9.8
        b2UZR = (((float(self.B2) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.295 - 19.5
        b3UZR = (((float(self.B3) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.301 - 18.7
        cfUZR = (((float(self.CF) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.519 - 36.6
        lfUZR = (((float(self.LF) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.436 - 32.8
        rfUZR = (((float(self.RF) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.453 - 34.1
        cUZR = (((float(self.C) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.11337 - 11.281
        self.UZR = self.pickUZR(ssUZR, b1UZR, b2UZR, b3UZR, cfUZR, lfUZR, rfUZR, cUZR)

    def calcUZRP(self, consts):
        nIFRNG = (((float(self.IFRNG) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nIFARM = (((float(self.IFARM) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nTDP = (((float(self.TDP) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nIFERR = (((float(self.IFERR) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nOFRNG = (((float(self.OFRNG) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nOFARM = (((float(self.OFARM) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nOFERR = (((float(self.OFERR) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nCABI = (((float(self.CABI) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)
        nCARM = (((float(self.CARM) - consts.minRating) / consts.deltaMinMax) * consts.fieldCo + 1)

        self.CP = (((nCABI - 62.5)/25*9.75) + ((nCARM - 62.5)/25*21.25)+74)
        self.B1P = ( ( (nIFRNG - 62.5)/25*27.25) + ( (nIFARM - 62.5)/25*2.25 ) + ( (nTDP - 62.5)/25*2.5 ) + ( (nIFERR - 62.5)/25*13.75 ) + 113.5 )
        self.B2P = ( ( (nIFRNG - 62.5)/25*21.5) + ( (nIFARM - 62.5)/25*1.5 ) + ( (nTDP - 62.5)/25*9 ) + ( (nIFERR - 62.5)/25*8.25 ) + 64.5 )
        self.B3P = ( ( (nIFRNG - 62.5)/25*21.5) + ( (nIFARM - 62.5)/25*6.75 ) + ( (nTDP - 62.5)/25*3.5 ) + ( (nIFERR - 62.5)/25*7.75 ) + 66 )
        self.SSP = ( ( (nIFRNG - 62.5)/25*23.5) + ( (nIFARM - 62.5)/25*2 ) + ( (nTDP - 62.5)/25*8 ) + ( (nIFERR - 62.5)/25*7.5 ) + 50 )
        self.LFP = ( ( (nOFRNG - 62.5)/25*31.5) + ( (nOFARM - 62.5)/25*4.25 ) + ( (nOFERR - 62.5)/25*6.25 ) + 80 )
        self.CFP = ( ( (nOFRNG - 62.5)/25*43) + ( (nOFARM - 62.5)/25*1.75 ) + ( (nOFERR - 62.5)/25*3.5 ) + 39 )
        self.RFP = ( ( (nOFRNG - 62.5)/25*33.75) + ( (nOFARM - 62.5)/25*6.25 ) + ( (nOFERR - 62.5)/25*6.25 ) + 71 )

        ssUZR = (((float(self.SSP) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.365 - 22.4
        b1UZR = (((float(self.B1P) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.167 - 9.8
        b2UZR = (((float(self.B2P) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.295 - 19.5
        b3UZR = (((float(self.B3P) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.301 - 18.7
        cfUZR = (((float(self.CFP) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.519 - 36.6
        lfUZR = (((float(self.LFP) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.436 - 32.8
        rfUZR = (((float(self.RFP) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.453 - 34.1
        #cUZR = (((float(self.CP) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.46 - 15.6
        cUZR = (((float(self.CP) - consts.minRating)/consts.deltaMinMax) * consts.fieldCo + 1)*.11337 - 11.281
        self.UZRP = self.pickUZR(ssUZR, b1UZR, b2UZR, b3UZR, cfUZR, lfUZR, rfUZR, cUZR)

    def pickUZR(self, ssUZR, b1UZR, b2UZR, b3UZR, cfUZR, lfUZR, rfUZR, cUZR):
        if self.Position == "SS":
            return ssUZR
        elif self.Position == "1B":
            return b1UZR
        elif self.Position == "2B":
            return b2UZR
        elif self.Position == "3B":
            return b3UZR
        elif self.Position == "CF":
            return cfUZR
        elif self.Position == "LF":
            return lfUZR
        elif self.Position == "RF":
            return rfUZR

        return cUZR


    #very rough wSB
    def calcwSB(self, consts):
        nSTE = (((float(self.STE) - consts.minRating) / consts.deltaMinMax) * consts.stealingCo + 1)
        return  .00004 * nSTE * nSTE * nSTE - 0.005 * nSTE * nSTE + 0.209 * nSTE - 3.8

    @staticmethod
    def findPlayerByName(name):
        retval = Player.select().where(Player.Name == name).first()
        return retval

    @staticmethod
    def findPlayer(name, dob):
        retval = Player.select().where((Player.Name == name) & (Player.DOB == dob)).first()
        return retval


__author__ = 'cmayer'

from HTMLParser import HTMLParser
from LeagueConsts import LeagueConsts
from Player import Player
from DBController import DBController
from League import League

# This class will import stats files

class PlayersImporter(HTMLParser):
    #vars
    #state (string) ;  What state the importer is in: "Init, Headers, Table, End"

    def __init__(self, consts):
        HTMLParser.__init__(self)
        self.section = "Init"
        self.subSection = 0
        self.playerData = ""
        self.currentPlayer = None
        self.hasData = False
        self.index = 0
        self.headers = dict()
        self.leagueConsts = consts

    def loadStats(self, statsFile):
        fStatsFile = open(statsFile, "r")
        wholeFeed = fStatsFile.read()
        self.feed(wholeFeed)

    #The file will be an html file that is a simple table.  We need to pull all the data out of that table.
    #Everything else can be discarded.
    #We'll do this via a simple state machine.  States:
    #Init - searching for the start of the table
    #Table - reading the table one line at a time
    #End - finished!

    #Subsections of table:
    #0: not yet in table
    #1: Title, typically "Player List"
    #2: cell spacing
    #3: Headers
    #4+: individual player rows

    def handle_starttag(self, tag, attrs):
#        print "Encountered a start tag:", tag
        if self.section == "Init" and tag == "table":
            self.section = "Table"
        elif self.section == "Table":
            if tag == "tr":
                self.subSection += 1

    def handle_endtag(self, tag):
 #       print "Encountered an end tag :", tag
        if tag == "table":
            self.section = "End"
        elif self.section == "Table":
            if tag == "td" and self.subSection > 3:
                if self.currentData == "":
                    self.playerData += "0,"
                else:
                    self.playerData += self.currentData + ","
            elif tag == "th" and self.subSection == 3:
                theHeader = self.currentData
                while self.headers.has_key(theHeader):
                    theHeader += 'a'
                self.headers[theHeader] = self.index
                #print (theHeader + ":%d" % self.index)
                self.index += 1
            elif tag == "tr" and self.subSection > 3:
                #encounted an end of player row
                fieldArray = self.playerData.split(',')
                #query for player based on name (field 1) and date (field 4)
                #print 'processing ' + unicode(fieldArray[1], errors="ignore")
                newPlayer = Player.findPlayer(unicode(fieldArray[1], errors="ignore"), fieldArray[4])
                if newPlayer is None:
                    newPlayer = Player()
                newPlayer.initFromString(self.playerData, self.headers, self.leagueConsts)
                newPlayer.save()
                self.playerData = ""
        self.currentData = ""

    def handle_data(self, data):
        if self.section == "Table":
            if self.subSection == 3 and data.isspace() is False:
                self.currentData += data
            elif self.subSection > 3 and data.isspace() is False:
                #reading player data
                self.currentData += data.replace(',',' ')

    def doImport(self, fileName):
        self.loadStats(fileName)

    def draftPlayers(self, fileName):
        f = open(fileName, "r")
        playerList = f.read()
        playerArray = playerList.split(",")
        for playerName in playerArray:
            player = DBController.findPlayerByName(playerName)
            if player:
                player.drafted = 1
                player.save()

    def fixTriples(self):
        for player in Player.select():
            player.wOBA = player.calcWOBA(player.CON, player.GAP, player.POW, player.EYE, player.Ks, player.SPE)
            player.wOBAvL = player.calcWOBA(player.CONvL, player.GAPvL, player.POWvL, player.EYEvL, player.KvL, player.SPE)
            player.wOBAvR = player.calcWOBA(player.CONvR, player.GAPvR, player.POWvR, player.EYEvR, player.KvR, player.SPE)
            player.wOBAP = player.calcWOBA(player.CONP, player.GAPP, player.POWP, player.EYEP, player.KP, player.SPE)
            player.save()

    def fixStats(self):
        for player in Player.select():
            player.calcStats(self.leagueConsts)
            player.save()

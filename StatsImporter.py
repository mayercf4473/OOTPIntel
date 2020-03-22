__author__ = 'cmayer'

from html.parser import HTMLParser
from LeagueConsts import LeagueConsts
from Stats import Stats
from DBController import DBController
from League import League

# This class will import stats files

class StatsImporter(HTMLParser):
    #vars
    #state (string) ;  What state the importer is in: "Init, Headers, Table, End"

    def __init__(self, year):
        HTMLParser.__init__(self)
        self.section = "Init"
        self.subSection = 0
        self.playerData = ""
        self.currentPlayer = None
        self.hasData = False
        self.index = 0
        self.headers = dict()
        self.year = year

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
                newPlayer = Stats.findPlayer(unicode(fieldArray[1], errors="ignore"), fieldArray[4], self.year)
                if newPlayer is None:
                    newPlayer = Stats()
                newPlayer.initFromString(self.year, self.playerData, self.headers)
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

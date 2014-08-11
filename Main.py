__author__ = 'cmayer'

from StatsImporter import StatsImporter
from League import League
from DBController import DBController
from Player import Player

def main():
    print "Welcome to stats importer!"
    #LeagueConsts.initLeague(1,10, 1, 10)
    #importer = PlayersImporter()
    importer = StatsImporter(2014)
    dbController = DBController()
    dbController.checkInit('input/LeagueStruct.json')
    #importer.doImport("mlcall.htm")
    #importer.doImport("mlchou.htm")
    importer.doImport("pbf_stats.htm")
    #importer.doImport("mlcall.htm")
    #importer.draftPlayers('drafted.txt')
    #importer.fixTriples()

if __name__ == "__main__":
   main()


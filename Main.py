from LeagueConsts import LeagueConsts
from PlayersImporter import PlayersImporter

__author__ = 'cmayer'

from StatsImporter import StatsImporter
from League import League
from DBController import DBController
from Player import Player

def main():
    print "Welcome to stats importer!"
    #LeagueConsts.initLeague(1,10, 1, 10)
    dbController = DBController()
    dbController.checkInit()
    importer = PlayersImporter(LeagueConsts('input/wbl_LeagueStruct.json'))
    #importer = StatsImporter(2014)
    #importer.fixStats()
    importer.doImport("input/wbl_all.htm")
    #importer.doImport("mlchou.htm")
    #importer.doImport("pbf_stats.htm")
    #importer.doImport("mlcall.htm")
    #importer.draftPlayers('drafted.txt')
    #importer.fixTriples()

if __name__ == "__main__":
   main()


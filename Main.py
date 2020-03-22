import argparse

import BaseModel
from peewee import MySQLDatabase
from LeagueConsts import LeagueConsts
from PlayersImporter import PlayersImporter

__author__ = 'cmayer'

from StatsImporter import StatsImporter
from League import League
from DBController import DBController
from Player import Player

def main():
    print ("Welcome to stats importer!")
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", help="Schema name", default="ootp_players")
    parser.add_argument("--config", help="Json config file")
    parser.add_argument("--playerFile", help="Player file to import")
    args=parser.parse_args()
    BaseModel.TheDatabase.init(args.schema, user='ootp', password='ootp')
    BaseModel.TheDatabase.connect()
    dbController = DBController()
    dbController.checkInit()
    importer = PlayersImporter(LeagueConsts(args.config))
    #importer = StatsImporter(2014)
    importer.doImport(args.playerFile)
    #importer.fixStats()
    #importer.draftPlayers("input/drafted.txt")

if __name__ == "__main__":
   main()


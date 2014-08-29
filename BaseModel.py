__author__ = 'cmayer'

from peewee import *

TheDatabase = MySQLDatabase('pbf_players', user='ootp', password='ootp')

class BaseModel(Model):
    class Meta:
        database = TheDatabase



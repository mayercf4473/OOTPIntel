__author__ = 'cmayer'

from peewee import *

TheDatabase = MySQLDatabase('ootp_players', user='ootp', password='ootp')

class BaseModel(Model):
    class Meta:
        database = TheDatabase



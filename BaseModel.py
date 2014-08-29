__author__ = 'cmayer'

from peewee import *

TheDatabase =  MySQLDatabase(None)

class BaseModel(Model):
    class Meta:
        database = TheDatabase



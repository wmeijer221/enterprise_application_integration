#!/usr/bin/env python

from pymongo import MongoClient
from time import sleep
import sys
import logging

LOGGER = logging.getLogger(__name__)

class MongoDB:

  # MAX_RETRIES = 10
  TIMEOUT = 5

  def __init__(self, url, port, username, password, database, authSource="admin"):
    self.connection_url = "mongodb://{}:{}@{}:{}/{}?authSource={}".format(username, password, url, port, database, authSource)
    self.database_name = database
    self.session = self.__try_connect()


  def __try_connect(self):
    connected = False
    while not connected:
      LOGGER.info("Attempting to connect to MongoDB...")
      try:
        session = MongoClient(self.connection_url)
      except Exception as e:
        # print(e)
        LOGGER.error("Unable to connect to MongoDB, retyring in", self.TIMEOUT, "seconds...")
        sleep(self.TIMEOUT)
        continue
      else:
        connected = True
        LOGGER.info("MongoDB connected!")
        self.db = session[self.database_name]
      finally:
        sys.stdout.flush()

    return session


  def getSession(self):
    if not self.session:
      self.__try_connect()

    return self.session


  def getDB(self, database=None):
    if not self.session:
      self.__try_connect()

    return self.session[database or self.database_name]
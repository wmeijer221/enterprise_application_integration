#!/usr/bin/env python

import time
import requests
import json
from translator import OntologyTranslator


class RestApiScraper():

  def __init__(self, translator: OntologyTranslator, target='http://host.docker.internal:5000', endpoints=['/']):
    self.__target = target
    self.__endpoints = endpoints
    self.__translator = translator


  def run(self):
    for endpoint in self.__endpoints:
      attempts = 0
      try:
        r = requests.get(self.__target+endpoint['uri'])
      except:
        attempts += 1
        if attempts < 10:
          time.sleep(1)
          print("Retrying...")
        else:
          print("Unable to reach endpoint:", endpoint['uri'])

      print('Received:',r.json())
      print('Translated:',self.__translator.canonify(endpoint['uri'], r.json()))
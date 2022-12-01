#!/usr/bin/env python

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
      r = requests.get(self.__target+endpoint['uri'])
      
      print('Received:',r.json())
      print('Translated:',self.__translator.canonify(endpoint['uri'], r.json()))
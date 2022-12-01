#!/usr/bin/env python


class OntologyTranslator():

  def __init__(self, ontology):
    self.__ontology = {}
    self.__ontology = ontology


  def canonify(self, endpoint, data):
    for k in self.__ontology[endpoint].keys():
      if self.__ontology[endpoint][k] in data.keys():
        data[k] = data.pop(self.__ontology[endpoint][k])

    return data
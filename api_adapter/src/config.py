#!/usr/bin/env python

import yaml
import json


class Config():

  def __init__(self, cfg_path='./config.yaml'):
    self.__config = {}
    self.__cfg_path = cfg_path

    with open(cfg_path, 'r') as cfg_file:
      self.__config = yaml.safe_load(cfg_file)


  def getTarget(self):
    return self.__config['target']


  def getEndpoints(self):
    return self.__config['endpoints']


  def getOntology(self):
    ontology = {endpoint['uri']:endpoint['ontology'] for endpoint in self.__config['endpoints']}
    print("Ontolgy:", ontology)
    return ontology


if __name__ == 'main':
  cfg_path = './config.yaml'
  cfg = Config(cfg_path)

  print("Target:", cfg.getTarget())
  print("Endpoints:", cfg.getEndpoints())
  print("Ontology:", cfg.getOntology())
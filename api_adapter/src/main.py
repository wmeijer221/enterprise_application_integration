#!/usr/bin/env python

from config import Config
from scraper import RestApiScraper
from translator import OntologyTranslator


if __name__ == '__main__':
  cfg_path = './config.yaml'
  cfg = Config(cfg_path)

  translator = OntologyTranslator(cfg.getOntology())

  scraper = RestApiScraper(translator, cfg.getTarget(), cfg.getEndpoints())

  scraper.run()
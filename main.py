# encoding=utf8

import anyconfig
import sys

from consumers import PrintConsumer, GmailConsumer, FileConsumer
from searchagents.searcher import PokemonSearcher, GPSSpots, Filter
from searchagents.fpm.webdriver.agent import FPMWebdriverAgent
from multiprocessing.dummy import Pool as ThreadPool
from config import Config

reload(sys)
sys.setdefaultencoding('utf8')

config = Config(sys.argv[1])

spots = GPSSpots()
spots.add(config.latitude(), config.longitude())

email_config = config.email()
filter_config = config.filter()
mail_consumer = GmailConsumer(email_config, Filter(filter_config))

while True:
	PokemonSearcher(spots, FPMWebdriverAgent([PrintConsumer(), FileConsumer(), mail_consumer])).search(4)
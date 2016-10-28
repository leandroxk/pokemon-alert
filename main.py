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
mail_consumer = GmailConsumer(email_config.send_from(), 
	email_config.password(), 
	email_config.send_to(),
	email_config.gmap_key(), 
	Filter())

while True:
	PokemonSearcher(spots, FPMWebdriverAgent([PrintConsumer(), FileConsumer(), mail_consumer	])).search(3)	
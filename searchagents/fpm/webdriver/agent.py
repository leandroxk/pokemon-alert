import os
import time
import requests
import math
import signal
import hashlib

from retrying import retry
from fake_useragent import UserAgent
from pattern import HoneycombSearchPattern
from multiprocessing.dummy import Pool as ThreadPool
from pokemon import Pokemon, PokemonEncounter
from db.pokedex import Pokedex
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

FPM_DIAMETER = 400
TIMEOUT = 120

class FPMWebdriverAgent():
	
	def __init__(self, result_consumers):
		self._consumers = result_consumers

	def search(self, spot, loops_num):
		lat, lng = spot
		dests = HoneycombSearchPattern(lat, lng, loops_num, FPM_DIAMETER).get_destinations()

		driver = self.open_fpm(spot)
		for spot in dests:
			#try:
			result = self._search(driver, spot)
			for consumer in self._consumers:
				consumer.consume(result)
			#except Exception as e:
			#	print str(e)
			#	print 'Erro ao procurar pokemon no  FPM, recuperando...'
		
		driver.quit()

	def open_fpm(self, spot):
		driver = webdriver.Chrome()
		driver.maximize_window()

		self._set_geolocation(driver, spot)
		driver.get('https://fastpokemap.se/')
		driver.refresh()

		self._click(driver, 'close')
		self._click(driver, 'location')

		return driver

	def _click(self, driver, class_name):
		WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
		driver.find_element_by_class_name(class_name).click()

	@retry(stop_max_attempt_number=10)
	def _search(self, driver, spot):
		self._set_geolocation(driver, spot)
		self._click('scan')

		WebDriverWait(driver, TIMEOUT).until(
			EC.invisibility_of_element_located((By.CLASS_NAME, 'active')))

		elements = driver.find_elements_by_class_name('displaypokemon')
		return FPMSearchResult(elements)

	def _set_geolocation(self, driver, spot):
		geo_js = "window.navigator.geolocation.getCurrentPosition=function(success){ var position = {\"coords\" : {\"latitude\": \"%s\",\"longitude\": \"%s\"}}; success(position);}" % spot
		print geo_js
		driver.execute_script(geo_js);


class FPMSearchResult():

	def __init__(self, elements):
		self._elements = elements

	def pokemon(self):
		if not self._elements:
			return []

		pokedex = Pokedex()
		encounters = []
		for element in self._elements:
			try:
				id = element.get_attribute('data-pokeid')
				lat = element.get_attribute('data-lat')
				lng = element.get_attribute('data-lng')
				name = pokedex.name(id)
				expiration_ts = element.find_element_by_class_name('remainingtext').get_attribute('data-expire')
			except Exception, e:
				print 'pokemon disappears...'
				continue

			expiration = float(expiration_ts) / 1000
			spawn = ''

			hash_text = '%s%s%s' % (id, lat, lng)
			encounter_id = hashlib.sha1(hash_text.encode("UTF-8")).hexdigest()[:10]

			pokemon = Pokemon(id, name)
			encounters.append(PokemonEncounter(pokemon, lat, lng, expiration, spawn, encounter_id))

		return encounters

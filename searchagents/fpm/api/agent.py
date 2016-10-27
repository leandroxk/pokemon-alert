from retrying import retry
from fake_useragent import UserAgent
from pattern import HoneycombSearchPattern
from multiprocessing.dummy import Pool as ThreadPool
from pokemon import Pokemon, PokemonEncounter

import requests
import math
import signal

FPM_DIAMETER = 400

class FPMAgent():
	
	def __init__(self, result_consumers):
		self.thread_pool = ThreadPool(25)
		self._consumers = result_consumers

	def search(self, spot, loops_num):
		lat, lng = spot
		dests = HoneycombSearchPattern(lat, lng, loops_num, FPM_DIAMETER).get_destinations()
		self.thread_pool.map(self._search, dests)

	def _search(self, spot):
		lat, lng = spot
		payload = { 
			'key': 'allow-all', 
			'ts': 0,
			'lat': lat,
			'lng': lng
		}
		headers = {
			'User-Agent': UserAgent().chrome,
			'Origin': 'https://fastpokemap.se'
		}

		url = "https://api.fastpokemap.se/"
		json = self._get(url, payload, headers)

		for consumer in self._consumers:
			consumer.consume(FPMSearchResult(json))

	@retry(wait_fixed=1000, stop_max_attempt_number=200)
	def _get(self, url, params, headers):
		r = requests.get(url, params=params, headers=headers)
		json = r.json()

		if 'error' in json:
			error = json['error']
			if 'overload' == error:
				raise OverloadException()
			else:
				raise UnknownException(error)
		print json
		return json


class FPMSearchResult():

	def __init__(self, result_data):
		self._result_data = result_data

	def pokemon(self):
		if 'result' not in self._result_data:
			return []

		encounters = []
		for item in self._result_data['result']:
			if 'pokemon_id' in item:
				id = item['pokemon_id']
				lat = item['latitude']
				lng = item['longitude']
				expiration = float(item['expiration_timestamp_ms']) / 1000
				spawn = item['spawn_point_id']
				encounter_id = item['encounter_id']

				pokemon = Pokemon(id, id)
				encounters.append(PokemonEncounter(pokemon, lat, lng, expiration, spawn, encounter_id))

		return encounters


class OverloadException(Exception):

	def __init__(self):
		pass	


class UnknownException(Exception):

	def __init__(self, msg):
		self._msg = msg

	def __str__(self):
		return self._msg
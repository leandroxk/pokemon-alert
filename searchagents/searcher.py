
from consumers import PrintConsumer, GmailConsumer
from config import FilterConfig


class PokemonSearcher():

	def __init__(self, gps_spots, search_agent):
		self._spots = gps_spots
		self._agent = search_agent

	def search(self, radius):
		for spot in self._spots.all():
			self._agent.search(spot, radius)


class GPSSpots():

	def __init__(self):
		self._spots = []

	def add(self, lat, lng):
		self._spots.append((lat, lng))

	def all(self):
		return self._spots


class Filter():

	def __init__(self, filter_config):
		self._config = filter_config

	def accept(self, pokemon):
		names = self._config.names()
		return pokemon.name().lower() in (name.lower() for name in names)

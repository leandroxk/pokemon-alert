import anyconfig
import os

from unipath import Path
from os.path import expanduser

class Config():
	
	def __init__(self, place):
		home = expanduser("~")
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self._config = anyconfig.load([
			Path(dir_path, 'config.json'), 
			Path(*[home, '.pokemon', 'config.json'])
		])
		self._global = self._config['global']
		self._place = self._config['places'][place]

	def latitude(self):
		return float(self._place['latitude'])

	def longitude(self):
		return float(self._place['longitude'])

	def email(self):
		return EmailConfig(self._global)


class EmailConfig():

	def __init__(self, global_config):
		self._config = global_config['email']

	def send_from(self):
		return self._config['from']

	def password(self):
		return self._config['password']

	def send_to(self):
		return self._config['to']

	def gmap_key(self):
		return self._config['maps-key']
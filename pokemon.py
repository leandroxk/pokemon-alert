import time

from ntplib import NTPClient
from retrying import retry


class Pokemon():

    def __init__(self, pokemon_id, name):
        self.id = pokemon_id
        self.name = name


class PokemonEncounter():

    def __init__(self, pokemon, lat, lng, expiration, spawn, encounter_id):
        self.pokemon = pokemon
        self.lng = lng
        self.expiration = expiration
        self.lat = lat
        self.spawn = spawn
        self.encounter_id = encounter_id

    def is_valid(self):
        return self._current_time() < self.expiration;

    def remaining_secs(self):
        remaining_s = self.expiration - self._current_time()
        if remaining_s > 0:
            return int(remaining_s)

        return 0;

    def remaining_time(self):
    	secs = self.remaining_secs()
    	return '%2.0fm:%2.0fs' % ((secs / 60) % 60, secs % 60)

    def id(self):
    	return self.pokemon.id

    def name(self):
        return self.pokemon.name

    def get_map(self):
        return '%s,%s' % (self.lat, self.lng)

    @retry(stop_max_delay=10000)
    def _current_time(self):
        return time.time()
#    	try:
#    		return NTPClient().request('gps.ntp.br').tx_time
#    	except Exception, e:
#    		return time.time()

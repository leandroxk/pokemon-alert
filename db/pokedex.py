import json

from objectpath import *

class Pokedex():

    def name(self, pokemon_id):
        return self.info(pokemon_id)['ename']

    def __init__(self):
        self._db = self._load()

    def info(self, pokemon_id='', name=''):
        return self._db.execute("$.*[@.id is '%s' or @.ename is '%s']" % (str(pokemon_id).zfill(3), name)).next()

    def _load(self):
        with open('db/pokedex.json') as f:
            data = json.load(f)

        return Tree(data)


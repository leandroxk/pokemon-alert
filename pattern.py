import geopy
import math

from geopy.distance import VincentyDistance


class HoneycombSearchPattern():

	def __init__(self, ref_lat, ref_lng, cicles, cell_diameter):
		self._ref_lat = ref_lat
		self._ref_lng = ref_lng
		self._cicles = cicles
		self._cell_diameter = cell_diameter

	def get_destinations(self):
		destinations = [(self._ref_lat, self._ref_lng)]
		for cicle in range(1, self._cicles):
			destinations += self.get_single_cicle_destinations(cicle)

		return destinations

	def get_single_cicle_destinations(self, cicle_num):
		total_radius = self._cell_diameter * cicle_num
		bearing = self._calc_bearing(self._cell_diameter, total_radius)

		sum_bearing = 0
		destinations = []
		while sum_bearing < 360:
			dest_lat, dest_log = self._calc_destination(self._ref_lat, self._ref_lng, total_radius, sum_bearing)
			sum_bearing += bearing

			destinations.append((dest_lat, dest_log))

		return destinations

	def _calc_bearing(self, radius_mt, total_radius):
		return 360 / ((2 * math.pi * total_radius) / radius_mt)

	def _calc_destination(self, lat, lng, total_radius, bearing):
		origin = geopy.Point(lat, lng)
		destination = VincentyDistance(meters=total_radius).destination(origin, bearing)
		return destination.latitude, destination.longitude

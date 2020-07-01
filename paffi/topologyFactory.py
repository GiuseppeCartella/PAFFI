from paffi.node import Sensor, Cloud, Fog
from paffi.nodeCollection import SensorCollection, FogCollection, CloudCollection


class TopologyFactory:

    def create_node(self, type=None, number=None, lat=None, lng=None, address=None):
        if type == "sensors":
            return Sensor(number, lat, lng, address)
        elif type == "fog":
            return Fog(number, lat, lng, address)
        elif type == "cloud":
            return Cloud(number, lat, lng, address)

    def create_node_collection(self, type):
        if type == "sensors":
            return SensorCollection()
        elif type == "fog":
            return FogCollection()
        elif type == "cloud":
            return CloudCollection()

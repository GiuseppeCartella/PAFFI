from math import radians, cos, sin, asin, sqrt
from paffi.topologyComponent import TopologyComponent


class Link(TopologyComponent):
    def __init__(self, src_node=None, dst_node=None, delay=None, label=None):
        self.src_node = src_node
        self.dst_node = dst_node
        self.delay = delay
        self.label = label

    def get_src_node(self):
        return self.src_node

    def set_src_node(self, src_node):
        self.src_node = src_node

    def get_dst_node(self):
        return self.dst_node

    def set_dst_node(self, dst_node):
        self.dst_node = dst_node

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay

    def set_delay(self):
        self.delay = self._calc_distance()

    def scale_delay(self, k):
        self.delay *= k

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def _calc_distance(self):
        lng1 = float(self.src_node.get_lng())
        lat1 = float(self.src_node.get_lat())
        lng2 = float(self.dst_node.get_lng())
        lat2 = float(self.dst_node.get_lat())
        # radians -> deg
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        # haversine formula
        dlng = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # earth radius (KM)
        return c * r

    def as_dict(self):
        return {"src": self.src_node.get_number(), "dst": self.dst_node.get_number(), "delay": self.delay}
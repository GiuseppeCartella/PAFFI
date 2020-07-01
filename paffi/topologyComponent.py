from abc import ABC, abstractmethod


class TopologyComponent(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def add(self, topology_component):
        raise AttributeError

    def remove(self, topology_component):
        raise AttributeError

    def get_avg_delay(self):
        raise AttributeError

    def as_dict(self):
        raise AttributeError

    def scale_delay(self, k):
        raise AttributeError

    def get_type(self):
        raise AttributeError

    def get_child(self, i):
        raise AttributeError

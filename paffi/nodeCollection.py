from abc import abstractmethod
from paffi.topologyComponent import TopologyComponent


class NodeCollection(TopologyComponent):
    @abstractmethod
    def __init__(self):
        self.topology_components = {}

    def add(self, topology_component):
        self.topology_components[topology_component.get_number()] = topology_component

    def remove(self, topology_component):
        self.topology_components.pop(topology_component.get_number())

    def get_child(self, i):
        return self.topology_components[i]

    def as_dict(self):
        dict = {}
        for key, value in self.topology_components.items():
            dict[key] = value.as_dict()
        return dict

    @abstractmethod
    def get_type(self):
        pass


class SensorCollection(NodeCollection):
    def __init__(self):
        super(SensorCollection, self).__init__()

    def get_type(self):
        return "sensors"


class FogCollection(NodeCollection):
    def __init__(self):
        super(FogCollection, self).__init__()

    def get_type(self):
        return "fog"


class CloudCollection(NodeCollection):
    def __init__(self):
        super(CloudCollection, self).__init__()

    def get_type(self):
        return "cloud"

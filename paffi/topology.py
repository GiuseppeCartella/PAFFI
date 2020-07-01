from paffi.topologyComponent import TopologyComponent
from paffi.connectionPolicy import NaiveConnection


class Topology(TopologyComponent):
    def __init__(self):
        self.collections = {}
        self.connection_type = ""
        self.scenario = {}
        self.connection_policy = NaiveConnection()

    def add(self, topology_component):
        self.collections[topology_component.get_type()] = topology_component

    def remove(self, topology_component):
        del self.collections[topology_component.get_type()]

    def get_node_types(self):
        node_list = [collection for collection in self.collections if not collection.startswith(("delay_", "conn_"))]
        return node_list

    def get_avg_delay(self):
        n = 0
        delay = 0.0
        for collection in self.collections.values():
            if collection.get_type().startswith("delay_"):
                n += 1
                delay += collection.get_avg_delay()

        return delay / n

    def scale_delay(self, k):
        for key, collection in self.collections.items():
            if key.startswith(("delay_","conn_")):
                collection.scale_delay(k)

    def get_connection_type(self):
        return self.connection_type

    def set_connection_type(self, connection_type):
        self.connection_type = connection_type

    def get_scenario(self):
        return self.scenario

    def set_scenario(self, scenario):
        self.scenario = scenario

    def set_connection_policy(self, connection_policy):
        self.connection_policy = connection_policy

    def get_child(self, coll_type):
        return self.collections[coll_type]

    def as_dict(self):
        dict = {}
        dict["connection_type"] = self.connection_type
        dict["scenario"] = self.scenario

        for key, value in self.collections.items():
            dict[key] = value.as_dict()

        return dict

    def execute_connection(self):
        self.connection_policy.connect(self)

from paffi.topologyComponent import TopologyComponent


class LinkCollection(TopologyComponent):
    def __init__(self, type, src_type=None, dst_type=None):
        self.topology_components = {}
        self.type = type
        self.src_type = src_type
        self.dst_type = dst_type

    def add(self, topology_component):
        self.topology_components[topology_component.get_label()] = topology_component

    def remove(self, topology_component):
        self.topology_components.pop(topology_component.get_label())

    def populate(self, link_dict):
        self.topology_components = link_dict

    def get_avg_delay(self):
        delay = 0.0
        for link in self.topology_components.values():
            delay += link.get_delay()

        return delay / len(self.topology_components)

    def scale_delay(self, k):
        for link in self.topology_components.values():
            link.scale_delay(k)

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_src_type(self):
        return self.src_type

    def set_src_type(self, src_type):
        self.src_type = src_type

    def get_dst_type(self):
        return self.dst_type

    def set_dst_type(self, dst_type):
        self.dst_type = dst_type

    def get_child(self, i):
        return self.topology_components[i]

    def as_dict(self):
        dict={}
        for i in self.topology_components.values():
            dict[i.get_label()] = i.as_dict()
        return dict
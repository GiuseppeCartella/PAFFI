import json
from paffi import Topology, TopologyFactory, LinkCollection, Link


class FileManager:
    def __init__(self):
        pass

    def save_topology(self, topology, fout):
        with open(fout, "w") as f:
            json.dump(topology, f, indent=4)

    def load_topology(self, fin):
            with open(fin, 'r') as f:
                topology = json.load(f)
            return topology

    @staticmethod
    def from_dict_to_object(topology_dict):
        topology = Topology()
        topology_factory = TopologyFactory()
        topology.set_connection_type(topology_dict.pop("connection_type"))
        topology.set_scenario(topology_dict.pop("scenario"))

        for c in topology_dict:
            if not c.startswith(("delay_", "conn_")):
                node_collection = topology_factory.create_node_collection(c)
                for n in topology_dict[c]:
                    node = topology_factory.create_node(c)
                    for key in topology_dict[c][n]:
                        setattr(node, key, topology_dict[c][n][key])
                    node_collection.add(node)
                topology.add(node_collection)

            else:
                link_collection = LinkCollection(c, c.split("_")[1], c.split("_")[2])
                nod_coll_1 = topology.get_child(c.split("_")[1])
                nod_coll_2 = topology.get_child(c.split("_")[2])

                for i, l in enumerate(topology_dict[c]):
                    node_a = nod_coll_1.get_child(topology_dict[c][l]["src"])
                    node_b = nod_coll_2.get_child(topology_dict[c][l]["dst"])
                    link = Link(node_a, node_b, topology_dict[c][l]["delay"], str(node_a.get_number()) + "_" + str(node_b.get_number()))
                    link_collection.add(link)

                topology.add(link_collection)

        return topology

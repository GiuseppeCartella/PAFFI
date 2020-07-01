import argparse
import itertools
from filemanager import FileManager
from paffi.link import Link
from paffi.linkCollection import LinkCollection

# FIXME: RIGUARDARE TUTTI I CASI in cui abbiamo chiamato node_collection.topology_components---> da migliorare
# fixme: in questo modo mi espone l'implementazione---> da evitare

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Scenario file. Default: topology.json")
parser.add_argument('-l', '--list', nargs='+', help="List of links [format: <src_node>_<dst_node>]", required=True)
parser.add_argument("-o", "--output", help="Scenario output file. Default: delay_topology.json")
args = parser.parse_args()

infile = args.input if args.input else "topology.json"
outfile = args.output if args.output else "delay_topology.json"
input_link_list = args.list

file_manager = FileManager()
topology = FileManager.from_dict_to_object(file_manager.load_topology(infile))
node_types = topology.get_node_types()

for pair in itertools.product(node_types, repeat=2):
    if pair[0] + "_" + pair[1] in input_link_list:
        link_collection = LinkCollection("delay_" + pair[0] + "_" + pair[1], src_type=pair[0], dst_type=pair[1])
        link_list = {str(node_a.get_number()) + "_" + str(node_b.get_number()): Link(node_a, node_b) for node_a in topology.get_child(pair[0]).topology_components.values()
                     for node_b in topology.get_child(pair[1]).topology_components.values()}

        for link in link_list.values():
            link.set_delay()
            link.set_label(str(link.src_node.get_number()) + "_" + str(link.dst_node.get_number()))

        link_collection.populate(link_list)
        topology.add(link_collection)

file_manager.save_topology(topology.as_dict(), outfile)



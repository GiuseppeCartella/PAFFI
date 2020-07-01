import argparse
import random
import sys


# FIXME: RIGUARDARE TUTTI I CASI in cui abbiamo chiamato node_collection.topology_components.values()---> da migliorare
# fixme: in questo modo si espone l'implementazione---> da evitare
from filemanager import FileManager
from paffi import Topology, TopologyFactory

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', nargs='+', help='List of validated nodes with POI_<node_type>.txt format',
                    required=True)
parser.add_argument("-c", "--cardinalities", nargs='+', help='List of cardinalities to generate the subsample',
                    required=True)
parser.add_argument("-o", "--output", help="Name of output file. Default = topology.json")
args = parser.parse_args()

node_files = args.list
cardinality_list = args.cardinalities
fout = args.output if args.output else "topology.json"


def check_format(list):
    for file in list:
        if file.startswith("POI_") and file.endswith(".txt"):
            continue
        else:
            return False
    return True


if len(node_files) != len(cardinality_list):
    sys.exit("Lists must have same length!")

try:
    cardinality_list = list(map(int, cardinality_list))
except ValueError:
    sys.exit("Cardinalities must be integer!")

if check_format(node_files) is False:
    sys.exit("Some files don't respect the format!")

topology = Topology()
topology_factory = TopologyFactory()
file_manager = FileManager()

for file, cardinality in zip(node_files, cardinality_list):
    with open(file) as f:
        lines = f.readlines()
        cardinality = cardinality if 0 <= cardinality <= len(lines) else len(lines)
        lines = random.sample(lines, cardinality)
        node_collection = topology_factory.create_node_collection(file[4:-4])

        for i, line in enumerate(lines):
            line = line.rstrip("\n")
            line = line.split("\t")
            node = topology_factory.create_node(file[4:-4], i, lat=float(line[1]), lng=float(line[2]), address=line[0])
            node_collection.add(node)

    topology.add(node_collection)

file_manager.save_topology(topology.as_dict(), fout)
import argparse
from filemanager import FileManager

#FIXME: RIGUARDARE TUTTI I CASI in cui abbiamo chiamato node_collection.topology_components---> da migliorare
#fixme: in questo modo mi espone l'implementazione---> da evitare


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help=".json input file for topology. Default = delay_topology.json")
parser.add_argument("-d", "--delta", help="Average network delay. Default = 10e-3")
parser.add_argument("-m", "--deltamu", help="delta_mu parameter. Default = 1")
parser.add_argument("-r", "--rho", help="rho parameter. Default = 0.5")
parser.add_argument("-o", "--output", help="Name for output file. Default = scenario.json")
args = parser.parse_args()

infile = args.input if args.input else "delay_topology.json"
outfile = args.output if args.output else "scenario.json"
file_manager = FileManager()

topology = FileManager.from_dict_to_object(file_manager.load_topology(infile))


delta = float(args.delta) if args.delta else 10e-3
delta_mu = float(args.deltamu) if args.deltamu else 1.0
rho = float(args.rho) if args.rho else 0.5

topology.set_scenario({"delta": delta, "delta_mu": delta_mu, "rho": rho})
d = topology.get_avg_delay()

topology.scale_delay(delta / d)

sensors_collection = topology.get_child("sensors")
fog_collection = topology.get_child("fog")

mu_fog = delta_mu / delta
lambda_src = rho * mu_fog * (len(fog_collection.topology_components) / len(sensors_collection.topology_components))

for sens in topology.get_child("sensors").topology_components.values():
    sens.set_lambda_sens(lambda_src)

for fog in topology.get_child("fog").topology_components.values():
    fog.set_mu(mu_fog)

file_manager.save_topology(topology.as_dict(), outfile)



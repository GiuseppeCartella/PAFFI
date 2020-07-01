import argparse

from paffi.connectionPolicy import AMPLConnection
from filemanager import FileManager

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Scenario file. Default: scenario.json")
parser.add_argument('-o', '--output', help="Output file [.json] for connected topology. Default: conn_topology.json")
parser.add_argument("-a", "--ampl", help="AMPL output for topology mapping. Default = None (use nearest fog for mapping)")
args = parser.parse_args()

infile = args.input if args.input else "scenario.json"
outfile = args.output if args.output else "conn_topology.json"

file_manager = FileManager()
topology = FileManager.from_dict_to_object(file_manager.load_topology(infile))

if args.ampl:
    topology.set_connection_policy(AMPLConnection(args.ampl))

topology.execute_connection()
file_manager.save_topology(topology.as_dict(), outfile)


import argparse
from paffi.connectionPolicy import AMPLConnection
from filemanager import FileManager

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help=".json input file for topology. Default = scenario.json")
parser.add_argument("-o", "--output", help="Name for output file. Default = problem.dat")
args = parser.parse_args()

infile = args.input if args.input else "scenario.json"
out = args.output if args.output else "problem"

file_manager = FileManager()
topology = file_manager.from_dict_to_object(file_manager.load_topology(infile))
ampl_connection = AMPLConnection(out)

ampl_connection.write_ampl_data(topology)
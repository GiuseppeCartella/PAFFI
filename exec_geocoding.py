import argparse
import sys
from geocoding.geocoder import Geocoder
from geocoding.validator import Validator

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help=".txt input file for street list", required=True)
parser.add_argument("-o", "--output", help=".txt output file. Default=validatedPOIs.txt")
args = parser.parse_args()

inputfile = args.input
outputfile = args.output if args.output else "validatedPOIs.txt"

geocoder = Geocoder()
validator = Validator()


if not inputfile.endswith(".txt") or not outputfile.endswith(".txt"):
    parser.print_help()
    sys.exit("Some files don't respect the format [.txt]")


try:
    with open(inputfile) as f, open(outputfile, 'w') as out:
        for street in f:
            line = street.rstrip()
            location = geocoder.do_geocode(line)
            if location:
                line = line + "\t" + "{:.9f}".format(location.latitude) + "\t" + "{:.9f}".format(location.longitude) + "\t"
                if 'suburb' in location.raw['address']:
                    line = line + location.raw['address']['suburb']

            result = validator.check(line)
            if result is True:
                out.write(line + "\n")
except FileNotFoundError:
    print("File not found, please insert a valid name.")

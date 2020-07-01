from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time


class Geocoder:
    def __init__(self):
        self.__geopy = Nominatim(user_agent="PAFFI framework")

    def do_geocode(self, address):
        time.sleep(1)
        try:
            return self.__geopy.geocode(address, addressdetails=True)
        except GeocoderTimedOut:
            return self.do_geocode(address)

    def do_geocode_reverse(self, latitude, longitude):
        time.sleep(1)
        try:
            return self.__geopy.reverse(latitude, longitude)
        except GeocoderTimedOut:
            return self.do_geocode_reverse(latitude, longitude)

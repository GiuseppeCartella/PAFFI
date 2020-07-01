from abc import abstractmethod
from paffi.topologyComponent import TopologyComponent


class Node(TopologyComponent):
    @abstractmethod
    def __init__(self, number=None, lat=None, lng=None, address=None):
        self.number = number
        self.lat = lat
        self.lng = lng
        self.address = address

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_lat(self):
        return self.lat

    def set_lat(self, lat):
        self.lat = lat

    def get_lng(self):
        return self.lng

    def set_lng(self, lng):
        self.lng = lng

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def as_dict(self):
        return vars(self)


class Sensor(Node):
    def __init__(self, number=None, lat=None, lng=None, address=None, lambda_sens=None):
        super(Sensor, self).__init__(number, lat, lng, address)
        self.lambda_sens = lambda_sens

    def get_lamda_sens(self):
        return self.lambda_sens

    def set_lambda_sens(self, lambda_sens):
        self.lambda_sens = lambda_sens


class Fog(Node):
    def __init__(self, number=None, lat=None, lng=None, address=None, mu=None):
        super(Fog, self).__init__(number, lat, lng, address)
        self.mu = mu

    def get_mu(self):
        return self.mu

    def set_mu(self, mu):
        self.mu = mu


class Cloud(Node):
    def __init__(self, number=None, lat=None, lng=None, address=None):
        super(Cloud, self).__init__(number, lat, lng, address)

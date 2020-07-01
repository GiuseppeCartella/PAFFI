class Validator:

    def _isfloat(self, s):
        try:
            float(s)
        except ValueError:
            return False
        return True

    def _valid(self, t):
        # tuple format: ('name', 'latitude', longitude, 'neighborhood name')
        try:
            if t[0].isnumeric():
                return False
            if not self._isfloat(t[1]):
                return False
            if not self._isfloat(t[2]):
                return False
            if t[3].isnumeric():
                return False
        except IndexError:
            return False
        # check if latitude and longitude are OK
        if (float(t[1]) < -90.0) or (float(t[1]) > 90.0):
            return False
        if (float(t[2]) < -180.0) or (float(t[2]) > 180.0):
            return False
        return True

    def check(self, line):
        line = line.rstrip("\n")
        line = line.split("\t")
        if len(line) == 4:
            if self._valid(line):
                return True
        return False

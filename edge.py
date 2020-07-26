from math import sqrt, pow


class Edge:

    def __init__(self, id, source, destination):
        self.weight = sqrt(pow((source.x - destination.x), 2) + pow((source.y - destination.y), 2))
        self.source = source
        self.destination = destination
        self.id = id

    def __repr__(self):
        return "[{}, {}, {}]".format(self.source, self.destination, round(self.weight, 2))

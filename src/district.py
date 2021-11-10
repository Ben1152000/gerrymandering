import random

from .utils import *

class Districting:

    # dict from precinct to district number
    # set of precincts in each district

    def __init__(self, state, number = 1):
        self.state = state

        # create list of districts (sets of precincts)
        self.districts = [set(self.state.precincts)]
        for i in range(number - 1):
            self.districts.append(set())
        assert len(self.districts) == number
        
        # create map from precinct to district
        self.map = dict()
        for precinct in self.state.precincts:
            self.map[precinct] = 0

        self.check_continuity()

    def check_continuity(self):
        """ensure districts are all contiguous"""
        for district in self.districts:
            if len(district):
                contiguous = set()
                queue = [next(iter(district))]
                while len(queue):
                    precinct = queue.pop(0)
                    if precinct not in contiguous:
                        contiguous.add(precinct)
                        for neighbor in precinct.neighbors:
                            if neighbor in district:
                                queue.append(neighbor)
                assert len(contiguous) == len(district)
    
    def flip(self):
        # select random precinct, district to flip to
        precinct = random.choice(self.state.precincts)
        new_district = random.randrange(len(self.districts))

        # ensure precinct borders the new district
        contiguous = (len(self.districts[new_district]) == 0)
        for neighbor in precinct.neighbors:
            if self.map[neighbor] == new_district:
                contiguous = True
        
        # TODO ensure old district is still contiguous
        old_district = self.map[precinct]
        contiguous = contiguous and True

        # if the flip is valid, make it
        if contiguous:
            self.districts[old_district].remove(precinct)
            self.districts[new_district].add(precinct)
            self.map[precinct] = new_district

        print(precinct.data['id'], old_district, new_district)

        # TODO update compactness measures

    def rejigger(self):
        """Select two districts at random and merge them, creating a new boundary between them"""
        # select two districts at random and check if they border each other
        # construct a random spanning tree on their graph
        # select a random edge to cut
        # update compactness measures
        pass

    def compactness(self):
        # possible compactness metrics:
        # - isoperimetric quotient (area over area of circle w/same perimeter)
        # - total perimeter over total area
        # - total circumscribed area over total area
        # - area of convex hull over total area
        # - perimeter of convex hull over total area
        # - weighting based on how much of the boundaries are county lines
        pass

    def to_svg(self, scale=10000.0):
        return self.state.to_svg(selector=lambda precinct: randomColor(self.map[precinct]), scale=10000.0)


class Districting:

    # dict from precinct to district number
    # set of precincts in each district

    def __init__(self, state, number = 1):
        # create list of districts (sets of precincts)
        self.districts = [state.precincts]
        for i in range(number - 1):
            self.districts.append(set())
        assert len(self.districts) == number
        
        # create map from precinct to district
        self.map = dict()
        for precinct in state.precincts:
            self.map[precinct] = 0

        # ensure district is contiguous
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
        # ensure contiguity of old and new districts
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

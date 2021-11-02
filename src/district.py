
class District:

    def __init__(self, precincts):
        self.precincts = precincts

        # ensure district is contiguous
        contiguous = set(next(iter(self.precincts)))
        for precinct in contiguous:
            for neighbor in precinct.neighbors:
                if neighbor in self.precincts:
                    contiguous.add(neighbor)

        assert len(contiguous) == len(self.precincts)

    def compactness(self):
        pass
        # possible compactness metrics:
        # - isoperimetric quotient (area over area of circle w/same perimeter)
        # - total perimeter over total area
        # - total circumscribed area over total area
        # - area of convex hull over total area
        # - perimeter of convex hull over total area
        # - weighting based on how much of the boundaries are county lines

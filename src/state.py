import fiona
from .precinct import Precinct

class State:
    
    def __init__(self, precincts):
        self.precincts = precincts

        # calculate bounding box
        precinct = next(iter(self.precincts))
        self.min_x = precinct.min_x
        self.max_x = precinct.max_x
        self.min_y = precinct.min_y
        self.max_y = precinct.max_y
        for precinct in self.precincts:
            if precinct.min_x < self.min_x:
                self.min_x = precinct.min_x
            if precinct.max_x > self.max_x:
                self.max_x = precinct.max_x
            if precinct.min_y < self.min_y:
                self.min_y = precinct.min_y
            if precinct.max_y > self.max_y:
                self.max_y = precinct.max_y

    @staticmethod
    def from_shapefile(filename):
        precincts = set()
        with fiona.open(filename) as source:
            for feature in source:
                # print(feature)
                if feature['geometry']['type'] == 'Polygon':
                    precincts.add(
                        Precinct(
                            county=feature['properties']['CNTY'],
                            id=feature['id'], 
                            polycoords=[feature['geometry']['coordinates']]
                        )
                    )
                elif feature['geometry']['type'] == 'MultiPolygon':
                    precincts.add(
                        Precinct(
                            county=feature['properties']['CNTY'],
                            id=feature['id'], 
                            polycoords=feature['geometry']['coordinates']
                        )
                    )
        return State(precincts)

    def to_svg(self):
        data = f'<svg viewBox="{0} {0} {round(self.max_x - self.min_x, 4)} {round(self.max_y - self.min_y, 4)}" xmlns="http://www.w3.org/2000/svg">\n'
        data += f'<rect x="{0}" y="{0}" width="{round(self.max_x - self.min_x, 4)}" height="{round(self.max_y - self.min_y, 4)}" fill="#ffffff" />\n'
        for precinct in self.precincts:
            data += precinct.to_svg(base=(self.min_x, self.min_y))
        data += '</svg>'
        return data

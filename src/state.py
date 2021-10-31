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

        # compute neighbors
        sorted(self.precincts, key=lambda precinct: precinct.min_x)
        # for precinct in self.precincts:
        #     print(precinct.min_x)

    @staticmethod
    def from_shapefile(filename):
        precincts = set()
        with fiona.open(filename) as source:
            for feature in source:
                # print(feature)
                
                polycoords = feature['geometry']['coordinates']
                if feature['geometry']['type'] == 'Polygon':
                    polycoords = [polycoords]

                precincts.add(
                    Precinct(
                        id=feature['id'], 
                        county=0,#feature['properties']['CNTYKEY'],
                        polycoords=polycoords,
                        voters={
                            # 'total': feature['properties']['G20VR'],
                            'trump': feature['properties']['G20PRERTRU'],
                            'biden': feature['properties']['G20PREDBID'],
                            'other': feature['properties']['G20PRELJOR']
                                # + feature['properties']['G20PREGHAW']
                                # + feature['properties']['G20PREOWRI']
                        },
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

import math
from shapely.geometry import MultiPolygon

# from .polygon import Polygon
from .utils import *

class Precinct:
    
    def __init__(self, id, polycoords, county, voters={}):
        self.id = id
        self.geometry = MultiPolygon([(coords[0], coords[1:]) for coords in polycoords])
        self.neighbors = set()
        self.county = county
        self.voters = voters

    def bounds(self):
        return self.geometry.bounds

    def length(self):
        return self.geometry.length

    def area(self):
        return self.geometry.area

    def point(self):
        return self.geometry.representative_point()

    def partisan_lean(self):
        if self.voters['biden'] + self.voters['trump'] == 0:
            return None
        return self.voters['biden'] / (self.voters['biden'] + self.voters['trump'])

    def to_svg(self, base=(0, 0, 0, 0), stroke=0):
        lean = self.partisan_lean()
        if lean is None:
            fill = 'grey'
        elif lean < 0.5:
            fill = f'#ff{int(lean * 2 * 255):02x}{int(lean * 2 * 255):02x}'
        else:
            fill = f'#{int((1 - lean) * 2 * 255):02x}{int((1 - lean) * 2 * 255):02x}ff'

        # fill = colorFromHue()

        data = f'<g id="precinct-{self.id}">\n'
        for polygon in self.geometry.geoms:
            polygon_data = ''

            points = ''
            for coords in polygon.exterior.coords:
                points += f'L{coords[0] - base[0]},{coords[1] - base[1]} '
            polygon_data += f'M{points[1:]}'

            for interior in polygon.interiors:
                points = ''
                for coords in interior.coords:
                    points += f'L{coords[0] - base[0]},{coords[1] - base[1]} '
                polygon_data += f'M{points[1:]}'
            
            data += f'<path fill="{fill}" stroke="black" stroke-width="{stroke}" d="{polygon_data} Z" />\n'
        data += '</g>\n'
        return data

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

    def bounds():
        return self.geometry.bounds

    def length():
        return self.geometry.length

    def area():
        return self.geometry.area

    def to_svg(self, base=(0, 0, 0, 0)):
        fill = colorFromHue(self.geometry.length)
        stroke = (base[2] - base[0] + base[3] - base[1]) / 10000.0

        data = f'<g id="precinct-{self.id}">\n'
        for polygon in self.geometry.geoms:
            polygon_data = ''

            points = ''
            for x, y in polygon.exterior.coords:
                points += f'L{x - base[0]},{y - base[1]} '
            polygon_data += f'M{points[1:]}'

            for interior in polygon.interiors:
                points = ''
                for x, y in interior.coords:
                    points += f'L{x - base[0]},{y - base[1]} '
                polygon_data += f'M{points[1:]}'
            
            data += f'<path fill="{fill}" stroke="black" stroke-width="{stroke}" d="{polygon_data} Z" />\n'
        data += '</g>\n'
        return data

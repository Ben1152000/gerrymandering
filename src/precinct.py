import math
from shapely.geometry import MultiPolygon

# from .polygon import Polygon
from .utils import *

class Precinct:
    
    def __init__(self, geometry, data=dict()):
        assert type(geometry) is MultiPolygon
        self.geometry = geometry
        self.neighbors = set()
        self.boundaries = dict()
        self.data = data

    def bounds(self):
        """Return the bounding box of the precinct geometry."""
        return self.geometry.bounds

    def length(self):
        """Return the total boundary length of the precinct geometry."""
        return self.geometry.length

    def area(self):
        """Return the total area of the precinct geometry."""
        return self.geometry.area

    def point(self):
        """Return a representative point guaranteed to be within the precinct."""
        return self.geometry.representative_point()

    def lean(self):
        """Return the percentage of democratic voters in the precinct."""
        
        if 'voters' not in self.data:
            return None
        voters = self.data['voters']
        if 'biden' not in voters or 'trump' not in voters:
            return None
        biden = voters['biden']
        trump = voters['trump']
        if biden + trump == 0:
            return None
        return biden / (biden + trump)

    def to_svg(self, base=(0, 0, 0, 0), stroke=0, color='grey'):
        """Convert the precinct to a svg vector image."""

        data = f'<g>\n'
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
            
            data += f'<path fill="{color}" stroke="black" stroke-width="{stroke}" d="{polygon_data} Z" />\n'
        data += '</g>\n'
        return data

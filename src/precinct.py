import math
from .polygon import Polygon
from .utils import *

class Precinct:
    
    def __init__(self, id, county, polycoords, voters={}):
        self.id = id
        self.county = county
        self.polygons = set()
        self.voters = voters

        for coords in polycoords:
            self.polygons.add(
                Polygon(
                    coords=coords[0], 
                    holes=coords[1:]
                )
            )
        
        # calculate bounding box
        polygon = next(iter(self.polygons))
        self.min_x = polygon.min_x
        self.max_x = polygon.max_x
        self.min_y = polygon.min_y
        self.max_y = polygon.max_y
        for polygon in self.polygons:
            if polygon.min_x < self.min_x:
                self.min_x = polygon.min_x
            if polygon.max_x > self.max_x:
                self.max_x = polygon.max_x
            if polygon.min_y < self.min_y:
                self.min_y = polygon.min_y
            if polygon.max_y > self.max_y:
                self.max_y = polygon.max_y

        self.neighbors = set()

    def to_svg(self, base=(0, 0)):
        color = randomColor(self.id)
        data = f'<g id="precinct-{self.id}">\n'
        polygon_id = 0
        for polygon in self.polygons:
            data += polygon.to_svg(
                id=f'{self.id}-{polygon_id}', base=base, fill=color
            )
            polygon_id += 1
        data += '</g>\n'
        return data

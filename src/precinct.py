from .polygon import Polygon
from .utils import randomColor

class Precinct:
    
    def __init__(self, county, id, polycoords):
        self.county = county
        self.id = id
        self.polygons = set()

        for coords in polycoords:
            self.polygons.add(
                Polygon(coords[0])
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

    def to_svg(self, base=(0, 0)):
        data = f'<g id="precinct-{self.id}">\n'
        for polygon in self.polygons:
            data += '\t' + polygon.to_svg(
                base=base, fill=randomColor(self.county + 1)
            ) + '\n'
        data += '</g>\n'
        return data

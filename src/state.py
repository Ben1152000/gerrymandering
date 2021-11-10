import fiona
from intervaltree import IntervalTree
from shapely.geometry import MultiPolygon
from scipy.spatial import KDTree

from .precinct import Precinct

class State:
    
    def __init__(self, precincts):
        self.precincts = precincts

        # calculate bounding box
        print('Calculating bounding boxes...')
        self.bounds = next(iter(self.precincts)).geometry.bounds
        for precinct in self.precincts:
            self.bounds = (
                min(self.bounds[0], precinct.geometry.bounds[0]),  # min_x
                min(self.bounds[1], precinct.geometry.bounds[1]),  # min_y
                max(self.bounds[2], precinct.geometry.bounds[2]),  # max_x
                max(self.bounds[3], precinct.geometry.bounds[3]),  # max_y
            )
        
        # compute neighbors for each precinct
        print('Calculating candidates for neighboring precincts...')
        begins = sorted(
            self.precincts,
            key=lambda precinct: precinct.geometry.bounds[0]
        )
        ends = sorted(
            self.precincts, 
            key=lambda precinct: precinct.geometry.bounds[2]
        )

        # defined as the margin of error for overlapping bounding boxes
        EPSILON = (self.bounds[2] - self.bounds[0] + self.bounds[3] - self.bounds[1]) / 10000.0

        # use an interval tree to calculate intersections of bounding boxes
        tree = IntervalTree()
        i = j = 0
        while (i < len(begins) and j < len(ends)):
            if (begins[i].geometry.bounds[0] - EPSILON < ends[j].geometry.bounds[2] + EPSILON):
                tree.addi(begins[i].geometry.bounds[1] - EPSILON, begins[i].geometry.bounds[3] + EPSILON, begins[i])
                i += 1
            else:
                tree.removei(ends[j].geometry.bounds[1] - EPSILON, ends[j].geometry.bounds[3] + EPSILON, ends[j])
                for interval in tree.overlap(ends[j].geometry.bounds[1] - EPSILON, ends[j].geometry.bounds[3] + EPSILON):
                    ends[j].neighbors.add(interval.data)
                    interval.data.neighbors.add(ends[j])
                j += 1
        while (j < len(ends)):
            tree.removei(ends[j].geometry.bounds[1] - EPSILON, ends[j].geometry.bounds[3] + EPSILON, ends[j])
            for interval in tree.overlap(ends[j].geometry.bounds[1] - EPSILON, ends[j].geometry.bounds[3] + EPSILON):
                ends[j].neighbors.add(interval.data)
                interval.data.neighbors.add(ends[j])
            j += 1

        # test whether shapes whose bounding boxes intersect actually intersect
        print('Pruning neighboring precincts...')
        for precinct in self.precincts:
            true_neighbors = set()
            for neighbor in precinct.neighbors:
                if neighbor.geometry.intersects(precinct.geometry):
                    true_neighbors.add(neighbor)
            precinct.neighbors = true_neighbors

    @staticmethod
    def from_shapefile(filename):
        print('Reading shapefile data...')
        precincts = []  # this should really be a set, but you can select a random item from a set in python
        
        with fiona.open(filename) as source:
            for feature in source:
                
                polycoords = feature['geometry']['coordinates']
                if feature['geometry']['type'] == 'Polygon':
                    polycoords = [polycoords]
                # geometry = MultiPolygon([(coords[0], coords[1:]) for coords in polycoords])
                geometry = MultiPolygon([([coord[0:2] for coord in coords[0]], [[coord[0:2] for coord in hole] for hole in coords[1:]]) for coords in polycoords])

                data = {
                    'id': int(feature['id']),
                    'county': int(feature['properties']['COUNTY']),
                    'voters': {
                        # 'total': feature['properties']['G20VR'],
                        'trump': feature['properties']['G20PRERTRU'],
                        'biden': feature['properties']['G20PREDBID'],
                        'other': feature['properties']['G20PRELJOR']
                            # + feature['properties']['G20PREGHAW']
                            # + feature['properties']['G20PREOWRI']
                    }
                }
                
                precincts.append(Precinct(geometry=geometry, data=data))
                
        return State(precincts)

    def to_svg(self, selector=(lambda precinct: 'grey'), scale=10000.0):
        """Displays the state as an svg, using a colorSelector lambda function that takes in the precinct and returns the color in hex."""
        scale = (self.bounds[2] - self.bounds[0] + self.bounds[3] - self.bounds[1]) / scale
        
        print('Generating vector image...')
        data = f'<svg viewBox="{0} {0} {self.bounds[2] - self.bounds[0]} {self.bounds[3] - self.bounds[1]}" xmlns="http://www.w3.org/2000/svg">\n'

        data += f'<rect x="{0}" y="{0}" width="{self.bounds[2] - self.bounds[0]}" height="{self.bounds[3] - self.bounds[1]}" fill="#ffffff" />\n'
        for precinct in self.precincts:
            data += precinct.to_svg(base=self.bounds, stroke=scale, color=selector(precinct))
        
        # Graph of neighboring precincts:
        for precinct in self.precincts:
            for neighbor in precinct.neighbors:
                data += f'<line x1="{precinct.point().x - self.bounds[0]}" y1="{precinct.point().y - self.bounds[1]}" x2="{neighbor.point().x - self.bounds[0]}" y2="{neighbor.point().y - self.bounds[1]}" stroke="black" stroke-width="{scale * 3}" />\n'
        for precinct in self.precincts:
            data += f'<circle cx="{precinct.point().x - self.bounds[0]}" cy="{precinct.point().y - self.bounds[1]}" r="{scale * 6}" stroke="black" fill="green" stroke-width="{scale * 3}" />\n'

        data += '</svg>'
        return data

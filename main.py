import sys
from src import State, Precinct, Districting
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPolygon

FILENAME = 'ne_vest_20'
NUM_DISTRICTS = 3

def main():

    state = State.from_shapefile(f'datasets/{FILENAME}/{FILENAME}.shp')
    
    with open('out.svg', 'w') as svg:
        svg.write(state.to_svg(scale=10000.0))

    districting = Districting(state, NUM_DISTRICTS)

if __name__ == "__main__":
    main()

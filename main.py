import sys
from src import State, Precinct, Districting, Selector
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPolygon

FILENAME = 'ne_vest_20'
NUM_DISTRICTS = 3

def main():

    state = State.from_shapefile(f'datasets/{FILENAME}/{FILENAME}.shp')
    
    with open('out.svg', 'w') as svg:
        svg.write(state.to_svg(selector=Selector.county))

    districting = Districting(state, NUM_DISTRICTS)

    for i in range(100000):
        districting.flip()

    with open('out.svg', 'w') as svg:
        svg.write(districting.to_svg())


if __name__ == "__main__":
    main()

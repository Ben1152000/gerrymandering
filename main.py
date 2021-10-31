import sys
from src import State

FILENAME = 'tx_vest_20'

def main():

    state = State.from_shapefile(f'{FILENAME}/{FILENAME}.shp')

    with open('out.svg', 'w') as svg:
        svg.write(state.to_svg())
    
    for precinct in state.precincts:
        for polygon in precinct.polygons:
            for point in polygon.points:
                print(point)

if __name__ == "__main__":
    main()

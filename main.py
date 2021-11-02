import sys
from src import State

FILENAME = 'ca_vest_20'

def main():

    state = State.from_shapefile(f'datasets/{FILENAME}/{FILENAME}.shp')

    with open('out.svg', 'w') as svg:
        svg.write(state.to_svg(scale=10000.0))
    
if __name__ == "__main__":
    main()

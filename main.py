import sys
from src import State

FILENAME = 'nh_vest_20'

def main():

    state = State.from_shapefile(f'{FILENAME}/{FILENAME}.shp')

    with open('out.svg', 'w') as svg:
        svg.write(state.to_svg())
    
if __name__ == "__main__":
    main()

import random, colorsys

def randomColor(seed=None):
    if seed is not None:
        random.seed(seed)
    hue = random.random()
    if seed is not None:
        random.seed()
    return colorFromHue(hue)

def colorFromHue(hue):
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
    return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


class Selector:
    """
    The following functions are implementations of colorSelector. That is, functions
    which take in a precinct as their argument and return the value of the color they
    should be in the svg.
    """

    @staticmethod
    def random(precinct):
        return randomColor(precinct.data['id']) if 'id' in precinct.data else 'grey'

    @staticmethod
    def county(precinct):
        return randomColor(seed=precinct.data['county']) if 'county' in precinct.data else 'grey'

    @staticmethod
    def partisan(precinct):
        lean = precinct.lean()
        if lean is None:
            return 'grey'
        elif lean < 0.5:
            return f'#ff{int(lean * 2 * 255):02x}{int(lean * 2 * 255):02x}'
        else:
            return f'#{int((1 - lean) * 2 * 255):02x}{int((1 - lean) * 2 * 255):02x}ff'

if __name__ == "__main__":
    print(randomColor(1))
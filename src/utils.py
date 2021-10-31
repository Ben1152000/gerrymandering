import random, colorsys

def randomColor(seed=None):
    if seed is None:
        random.seed(seed)
    hue = random.random()
    if seed is None:
        random.seed()
    return colorFromHue(hue)

def colorFromHue(hue):
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
    return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

if __name__ == "__main__":
    print(randomColor(1))
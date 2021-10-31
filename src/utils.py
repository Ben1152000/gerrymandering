import random, colorsys

def randomColor(seed):
    random.seed(seed)
    r, g, b = colorsys.hsv_to_rgb(random.random(), 0.8, 1.0)
    random.seed()
    return '#' + hex(int(r * 255))[2:] + hex(int(g * 255))[2:] + hex(int(b * 255))[2:]

if __name__ == "__main__":
    print(randomColor(1))
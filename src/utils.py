import random, colorsys

def randomColor(seed=None):
    if seed != None:
        random.seed(seed)
    else:
        random.seed()
    r, g, b = colorsys.hsv_to_rgb(random.random(), 0.8, 1.0)
    random.seed()
    return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

if __name__ == "__main__":
    print(randomColor(1))
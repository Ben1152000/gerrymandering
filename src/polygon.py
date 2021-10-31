
class Polygon:

    def __init__(self, coords):
        self.points = []
        for x, y in coords:
            self.points.append(
                (round(x, 4), round(y, 4))
            )

        # calculate bounding box
        self.min_x, self.min_y = self.max_x, self.max_y = self.points[0]
        for x, y in self.points:
            if x < self.min_x:
                self.min_x = x
            elif x > self.max_x:
                self.max_x = x
            if y < self.min_y:
                self.min_y = y
            elif y > self.max_y:
                self.max_y = y
    
    def to_svg(self, base=(0, 0), fill='#000000'):
        points = ''
        for x, y in self.points:
            points += f'{round(x - base[0], 4)}, {round(y - base[1], 4)} '
        return f'<polygon points="{points}" fill="{fill}" stroke="black" stroke-width="100" />'

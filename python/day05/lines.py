class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_string(self):
        return '[ x={}, y={} ]'.format(self.x, self.y)


class Dimension(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def to_string(self):
        return '[ width={}, height={} ]'.format(self.width, self.height)


class Line(object):

    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def get_points(self):
        points = []
        if self.is_horizontal():
            points = self._get_horizontal_points()
        elif self.is_vertical():
            points = self._get_vertical_points()
        elif self.is_diagonal():
            points = self._get_diagonal_points()
        return points

    def _get_horizontal_points(self):
        points = []
        start_x = min(self.start_point.x, self.end_point.x)
        end_x = max(self.start_point.x, self.end_point.x)
        for x in range(start_x, end_x + 1):
            points.append(Point(x, self.start_point.y))
        return points

    def _get_vertical_points(self):
        points = []
        start_y = min(self.start_point.y, self.end_point.y)
        end_y = max(self.start_point.y, self.end_point.y)
        for y in range(start_y, end_y + 1):
            points.append(Point(self.start_point.x, y))
        return points

    def _get_diagonal_points(self):
        points = []
        start_x = self.start_point.x
        if self.end_point.x >= self.start_point.x:
            step_x = 1
            end_x = self.end_point.x + 1
        else:
            step_x = -1
            end_x = self.end_point.x - 1

        start_y = self.start_point.y
        if self.end_point.y >= self.start_point.y:
            step_y = 1
        else:
            step_y = -1

        y = start_y
        for x in range(start_x, end_x, step_x):
            points.append(Point(x, y))
            y += step_y

        return points

    def is_horizontal(self):
        return self.start_point.y == self.end_point.y

    def is_vertical(self):
        return self.start_point.x == self.end_point.x

    def is_diagonal(self):
        return abs(self.start_point.y - self.end_point.y) == abs(self.start_point.x - self.end_point.x)

    def to_string(self):
        points_str = ''
        for point in self.get_points():
            points_str += point.to_string()
            points_str += ', '
        return 'start_point={}, end_point={}, points={}'.format(self.start_point.to_string(),
                                                                self.end_point.to_string(), points_str)


class LinesMap(object):

    def __init__(self):
        self.lines = []
        self.max_x = 0
        self.max_y = 0
        self.dimension = None
        self.point_counts = None

    def add_line(self, line):
        self.lines.append(line)
        if line.start_point.x > self.max_x:
            self.max_x = line.start_point.x
        if line.end_point.x > self.max_x:
            self.max_x = line.end_point.x
        if line.start_point.y > self.max_y:
            self.max_y = line.start_point.y
        if line.end_point.y > self.max_y:
            self.max_y = line.end_point.y
        
    def get_dimension(self):
        if self.dimension is None:
            self.dimension = Dimension(self.max_x + 1, self.max_y + 1)
        return self.dimension

    def get_point_counts(self):
        if self.point_counts is None:
            self.point_counts = self._calculate_point_counts()
        return self.point_counts

    def _calculate_point_counts(self):
        point_counts = [[0] * self.get_dimension().height for i in range(self.get_dimension().width)]
        self._count_points(point_counts)
        return point_counts

    def _count_points(self, point_counts):
        for line in self.lines:
            for point in line.get_points():
                point_counts[point.y][point.x] += 1

    def get_intersection_points_count(self):
        count = 0
        for row in self.get_point_counts():
            for value in row:
                if value > 1:
                    count += 1
        return count

    def to_string(self):
        result = 'line map:\ndimension={}\n'.format(self.get_dimension().to_string())
        for i in range(self.get_dimension().width):
            for j in range(self.get_dimension().height):
                result += '{} '.format('.' if self.get_point_counts()[i][j] == 0 else self.get_point_counts()[i][j])
            result += '\n'
        result += '\nlines:\n'
        for line in self.lines:
            result += line.to_string()
            result += '\n'
        return result


def _create_line(input_line):
    points = input_line.strip().split(' -> ')
    start_points = points[0].split(',')
    start_point = Point(int(start_points[0]), int(start_points[1]))
    end_points = points[1].split(',')
    end_point = Point(int(end_points[0]), int(end_points[1]))
    return Line(start_point, end_point)


def main():
    lines_map = LinesMap()
    with open('lines.data', 'r') as data_file:
        input_line = data_file.readline()
        while input_line:
            lines_map.add_line(_create_line(input_line))
            input_line = data_file.readline()
    print(lines_map.to_string())
    print('intersection_points_count={}'.format(lines_map.get_intersection_points_count()))


main()

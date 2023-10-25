import matplotlib.pyplot as plt
import sys

class LineSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.slope = (end[1] - start[1]) / (end[0] - start[0]) if start[0] != end[0] else float('inf')
        self.intercept = start[1] - self.slope * start[0]

def intersection(line1, line2):
    """
    Check if the two line segment Intersects and returns an intersection point if present
    :param line1: The First Line
    :param line2: The Second Line
    :return: Intersection point
    """
    # Check if two line segments intersect
    if (line1.start[0] == line1.end[0] and line2.start[0] == line2.end[0]) or (line1.slope == line2.slope):
        return None  # The segments are parallel or vertical, so they do not intersect

    if line1.start[0] == line1.end[0]:
        x = line1.start[0]
        y = line2.slope * x + line2.intercept
    elif line2.start[0] == line2.end[0]:
        x = line2.start[0]
        y = line1.slope * x + line1.intercept
    else:
        x = (line2.intercept - line1.intercept) / (line1.slope - line2.slope)
        y = line1.slope * x + line1.intercept

    if (min(line1.start[0], line1.end[0]) <= x <= max(line1.start[0], line1.end[0]) and
        min(line2.start[0], line2.end[0]) <= x <= max(line2.start[0], line2.end[0])):
        return x, y  # Intersection point
    else:
        return None


def get_points(filename):
    """
    Reads the points from the input file and stores in a list
    :param filename: input file name
    :return: a list of input points
    """
    points = []
    with open(filename) as f:
        for line in f:
            points.append([int(x) for x in line.rstrip().split()])

    points.pop(0)   # Removes the first element of the file from the list i.e. the number of points
    return points


def update_points(points, filename):
    """
    Updates the Convex Hull points to the output file
    :param filename: Name for the output file
    :param points: Points forming convex hull
    """
    n = str(len(points))
    with open(filename, "w") as f:
        f.write(n + "\n")
        for point in points:
            f.write(str(point[0]) + " " + str(point[1]) + "\n")


def plot_line_segments(segments):
    """
    Plot all the segments
    :param segments: given segments
    :return: None
    """
    for segment in segments:
        x = [segment.start[0], segment.end[0]]
        y = [segment.start[1], segment.end[1]]
        plt.plot(x, y, label="Segment", c='black')
        plt.scatter(segment.start[0], segment.start[1], c='b', s=5)
        plt.scatter(segment.end[0], segment.end[1], c='b', s=5)


def plot_intersection_points(intersection_points):
    """
    Plot all the intersections
    :param intersection_points: points
    :return: None
    """
    for point in intersection_points:
        plt.plot(point[0], point[1], 'ro', label="Intersection", markersize=2)


def find_all_intersections(segments):
    """
    Function to find all intersection points
    :param segments: list of segments
    :return: None
    """
    intersection_points = []
    for i, segment1 in enumerate(segments):
        for j, segment2 in enumerate(segments):
            if i < j:  # Avoid checking the same pair of segments twice
                intersect = intersection(segment1, segment2)
                if intersect:
                    intersection_points.append(intersect)
    return intersection_points


def main():
    filename = sys.argv[1]
    points = get_points(filename)
    segments = list()
    for i in points:
        if i[0] > i[2]:
            i[0], i[2] = i[2], i[0]
            i[1], i[3] = i[3], i[1]
        segments.append(LineSegment((i[0], i[1]), (i[2], i[3])))

    intersection_points = find_all_intersections(segments)
    update_points(intersection_points, 'output_bf.txt')

    plot_line_segments(segments)
    plot_intersection_points(intersection_points)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line Segment Intersection')
    plt.show()


if __name__ == '__main__':
    main()
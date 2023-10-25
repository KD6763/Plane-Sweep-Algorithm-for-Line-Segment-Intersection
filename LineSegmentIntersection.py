"""
file: LineSegmentIntersection.py
purpose: Runs Line Intersection using plane sweep algorithm
Author: Kedar Fitwe (kf3121@rit.edu)
"""


from sortedcontainers import SortedSet
import matplotlib.pyplot as plt
from bisect import bisect_right
import math
from matplotlib.animation import FuncAnimation
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Segment:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.slope = (right.y - left.y) / (right.x - left.x) if left.x != right.x else float('inf')
        self.intercept = left.y - self.slope * left.x
        self.key = (self.left.x, self.left.y)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __lt__(self, other):
        val = self.key[1] - (self.key[0] * other.slope) - other.intercept
        val = round_float(val, 5)
        if val == 0:
            return self.slope > other.slope
        return val > 0

    def __str__(self):
        s = "Segment: Left:" + str(self.left) + " Right: " + str(self.right) + " key:" + str(self.key)
        return s


class Sweep:
    def __init__(self):
        self.sweep_line = list()

    def add_item(self, item, key):
        item.key = key
        index = bisect_right(self.sweep_line, item)
        self.sweep_line.insert(index, item)

    def get_index(self, item):
        return self.sweep_line.index(item)

    def remove_item(self, item):
        self.sweep_line.remove(item)

    def get_item(self, index):
        return self.sweep_line[index]

    def get_length(self):
        return len(self.sweep_line)

    def __str__(self):
        s = "Sweep : \n"
        for i in self.sweep_line:
            s += str(i) + '\n'
        s += "End Sweep"
        return s


class Event:
    def __init__(self, x, y, is_left, is_intersect, line):
        self.x = x
        self.y = y
        self.is_left = is_left
        self.is_intersect = is_intersect
        self.line = line

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.is_intersect == other.is_intersect:
            return True
        return False

    def __hash__(self):
        return hash(self.x + self.y)

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __str__(self):
        s = "Event : x, y : " + str((self.x, self.y)) + " is_left : " + str(self.is_left) + " line: " + str(self.line)
        return s


def round_float(value, precision):
    """
    Rounds of the float value to given decimal precision
    :param value: Float value needed to be rounded off
    :param precision: decimal precision
    :return: Rounded off Float value
    """
    return math.floor(value * (10 ** precision)) / (10 ** precision)


def do_intersect(line1, line2):
    """
    Check if the two line segment Intersects and returns an intersection point if present
    :param line1: The First Line
    :param line2: The Second Line
    :return: Intersection point
    """
    if (line1.left.x == line1.right.x and line2.left.x == line2.right.x) or (line1.slope == line2.slope):
        return None  # The segments are parallel or vertical, so they do not intersect

    if line1.left.x == line1.right.x:
        x = line1.left.x
        y = line2.slope * x + line2.intercept
    elif line2.left.x == line2.right.x:
        x = line2.left.x
        y = line1.slope * x + line1.intercept
    else:
        x = (line2.intercept - line1.intercept) / (line1.slope - line2.slope)
        y = line1.slope * x + line1.intercept

    if (min(line1.left.x, line1.right.x) <= x <= max(line1.left.x, line1.right.x) and
            min(line2.left.x, line2.right.x) <= x <= max(line2.left.x, line2.right.x)):
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

    points.pop(0)  # Removes the first element of the file from the list i.e. the number of points
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


def plane_sweep(arr):
    """
    The Driver algorithm divided into 3 parts:
    1) Updating all the line segments as events and loading event one by one
    2) Deleting an event when executed
    3) Dealing with Intersection points as events
    :param arr: The input sample segments
    :return: List of intersection points
    """
    e = SortedSet()
    for i in range(len(arr)):
        e.add(Event(arr[i].left.x, arr[i].left.y, True, False, arr[i]))
        e.add(Event(arr[i].right.x, arr[i].right.y, False, False, arr[i]))

    s = Sweep()
    ans = 0
    res = []
    event_order = []
    while len(e) != 0:
        curr = e.pop(0)
        event_order.append(curr)
        if curr.is_left and not curr.is_intersect:
            print("------------------------------------------------------------------------------------------------")
            print("Getting an event")
            s.add_item(curr.line, (curr.x, curr.y))
            curr_s = s.get_index(curr.line)
            current_event = s.get_item(curr_s)

            if curr_s + 1 < s.get_length() and curr_s + 1 != 0:
                next_event = s.get_item(curr_s+1)
                if do_intersect(current_event, next_event) is not None:
                    x, y = do_intersect(current_event, next_event)
                    if x > curr.x:
                        e.add(Event(x, y, True, True, [current_event, next_event]))

            if 0 < curr_s-1 < s.get_length():
                prev_event = s.get_item(curr_s-1)
                if do_intersect(prev_event, current_event) is not None:
                    x, y = do_intersect(prev_event, current_event)
                    if x > curr.x:
                        e.add(Event(x, y, True, True, [prev_event, current_event]))

            if curr_s+1 < s.get_length() and curr_s+1 != 0 and 0 < curr_s-1 < s.get_length():
                next_event = s.get_item(curr_s + 1)
                prev_event = s.get_item(curr_s - 1)
                if do_intersect(prev_event, next_event) is not None:
                    x, y = do_intersect(prev_event, next_event)
                    if x > curr.x:
                        e.remove(Event(x, y, True, True, [prev_event, next_event]))

        elif not curr.is_left and not curr.is_intersect:
            
            print("------------------------------------------------------------------------------------------------")
            print("Deleting the event")
            curr_s = s.get_index(curr.line)
            current_event = s.get_item(curr_s)

            s.remove_item(current_event)
            if curr_s+1 < s.get_length() and curr_s+1 != 0 and 0 < curr_s-1 < s.get_length():
                next_event = s.get_item(curr_s + 1)
                prev_event = s.get_item(curr_s - 1)
                if do_intersect(prev_event, next_event) is not None:
                    x, y = do_intersect(prev_event, next_event)
                    if x > curr.x:
                        e.add(Event(x, y, True, True, [prev_event, next_event]))

        elif curr.is_intersect:
            print("------------------------------------------------------------------------------------------------")
            print("On Intersection")
            temp_lines = curr.line
            curr_first = s.get_index(temp_lines[0])
            current_top = s.get_item(curr_first)
            if 0 < curr_first-1 < s.get_length():
                prev_event = s.get_item(curr_first - 1)
                if do_intersect(prev_event, current_top) is not None:
                    x, y = do_intersect(prev_event, current_top)
                    if x > curr.x:
                        print("Removing intersections by top element if any")
                        e.remove(Event(x, y, True, True, [prev_event, current_top]))
            s.remove_item(current_top)

            curr_second = s.get_index(temp_lines[1])
            current_bottom = s.get_item(curr_second)
            if curr_second+1 < s.get_length() and curr_second+1 != 0:
                next_event = s.get_item(curr_second + 1)
                if do_intersect(current_bottom, next_event) is not None:
                    x, y = do_intersect(current_bottom, next_event)
                    if x > curr.x:
                        print("Removing intersections by bottom element if any")
                        e.remove(Event(x, y, True, True, [current_bottom, next_event]))
            s.remove_item(current_bottom)

            s.add_item(temp_lines[1], (curr.x, curr.y))
            curr_second = s.get_index(temp_lines[1])
            current_top = s.get_item(curr_second)
            if 0 < curr_second - 1 < s.get_length():
                prev_event = s.get_item(curr_second - 1)
                if do_intersect(prev_event, current_top) is not None:
                    x, y = do_intersect(prev_event, current_top)
                    if x > curr.x:
                        e.add(Event(x, y, True, True, [prev_event, current_top]))

            s.add_item(temp_lines[0], (curr.x, curr.y))
            curr_first = s.get_index(temp_lines[0])
            current_bottom = s.get_item(curr_first)
            if curr_first+1 < s.get_length() and curr_first+1 != 0:
                next_event = s.get_item(curr_first + 1)
                if do_intersect(current_bottom, next_event) is not None:
                    x, y = do_intersect(current_bottom, next_event)
                    if x > curr.x:
                        e.add(Event(x, y, True, True, [current_bottom, next_event]))

            res.append((curr.x, curr.y))
            ans += 1
        print(s)
    print("Total Number of Intersections", str(ans))
    return res, event_order


def plot_line_segments(segments, event_order):
    """
    Draws a plot for all the segments
    :param segments: Available segments
    :return: None
    """
    fig, ax = plt.subplots()
    for segment in segments:
        x = [segment.left.x, segment.right.x]
        y = [segment.left.y, segment.right.y]
        ax.plot(x, y, 'black', label="Segment", markersize=0.5)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line Segment Intersection')

    def update(frame, event_order):
        event = event_order[frame]
        if event.is_left and not event.is_intersect:
            ax.scatter(event.x, event.y, c='b', s=10, marker='o')
        elif not event.is_left and not event.is_intersect:
            ax.scatter(event.x, event.y, c='b', s=10, marker='o')
        else:
            ax.scatter(event.x, event.y, c='r', s=20, marker='o')
        ax.axvline(event.x, linestyle=':', c='slategray', lw=1, label='sweep')


    def animate(frame):
        update(frame, event_order)

    animate = FuncAnimation(fig, animate, frames=len(event_order), repeat=False)
    plt.show()



def main():
    filename = sys.argv[1]
    points = get_points(filename)
    segments = list()
    for i in points:
        if i[0] > i[2]:
            i[0], i[2] = i[2], i[0]
            i[1], i[3] = i[3], i[1]
        segments.append(Segment(Point(i[0], i[1]), Point(i[2], i[3])))

    intersections, event_order = plane_sweep(segments)
    update_points(intersections,'output_ps.txt')
    plot_line_segments(segments, event_order)


if __name__ == '__main__':
    main()

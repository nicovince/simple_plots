#!/usr/bin/env python
import math
import itertools
import operator
from sets import Set

class Point:
    '''Point with cartesian coordinates'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        '''Return string representation of Point'''
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        '''Test if two points are equals'''
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def mirror_y(self):
        '''Return symetrical point on y axis'''
        return Point(-self.x, self.y)

    def mirror_x(self):
        '''Return symetrical point on x axis'''
        return Point(self.x, -self.y)

    def mirror_xy(self):
        '''Return symetrical point from origin'''
        return Point(-self.x, -self.y)

    @staticmethod
    def snap(x, y):
        '''Snap point to the integer grid'''
        return (round(x), round(y))

    def offset(self, offset_x, offset_y):
        '''Apply offset to point'''
        self.x += offset_x
        self.y += offset_y

    def rotate(self, t):
        '''Rotate point at an angle t around origin'''
        m = [[math.cos(t), -math.sin(t)],[math.sin(t), math.cos(t)]]
        v = [self.x, self.y]
        self.x = sum(itertools.starmap(operator.mul, itertools.izip(v, m[0])))
        self.y = sum(itertools.starmap(operator.mul, itertools.izip(v, m[1])))

    def gp_str(self):
        '''Dump gnuplot point'''
        return str(self.x) + " " + str(self.y) + "\n"

    def gp_dump_boxxy(self):
        '''Dump data as boxxyerrorbars to draw a box instead of a single dot'''
        x_low = self.x
        x_high = self.x + 1
        y_low = self.y
        y_high = self.y + 1
        res = str(self.x) + " " + str(self.y)
        res += " " + str(x_low) + " " + str(x_high)
        res += " " + str(y_low) + " " + str(y_high)
        res += "\n"
        return res


class Plot(object):
    '''Plot object is a list of point with methods to display/dump datas for gnuplot'''
    def __init__(self):
        self.points = Set()

    def __str__(self):
        s = ""
        for p in self.points:
            s += str(p) + "\n"
        return s

    def dump(self, output="/dev/stdout"):
        '''Dump data to output file (default is stdout)'''
        f_out = open(output, "wb")
        for p in self.points:
             f_out.write(p.gp_dump_boxxy())

    def gp_script(self, script_name):
        '''Generate gnuplot script and dump data to file'''
        data_file = script_name + ".dat"
        # script
        f_out = open(script_name + ".gnu", "wb")
        # make sure x/y axes have same scale
        f_out.write("set size square\n")
        f_out.write("plot '" + data_file + "' with boxxyerrorbars\n")
        f_out.write("pause -1\n")
        f_out.write("# vim: set syntax=gnuplot:\n")

        # data file
        self.dump(data_file)


    def offset(self, offset_x, offset_y):
        '''Apply offset to all the points'''
        # NOTE: we are modifying the elements of the set we are currently iterating
        # I would expecte to have issue because modifying an element changes its hash
        # It looks like it is working though
        for p in self.points:
            p.offset(offset_x, offset_y)

    def get_xrange(self, margin=1):
        '''Get horizontal range for which graph will be displayed extanded by margin on both side'''
        minX = None
        maxX = None
        for p in self.points:
            if minX == None:
                minX = p.x
                maxX = p.x
            else:
                minX = min(minX, p.x)
                maxX = max(maxX, p.x)
        return (minX - margin, maxX  + margin)

    def get_gp_xrange(self):
        '''Return xrange for gnuplot script'''
        minX, maxX = self.get_xrange()
        return "[x = " + str(minX) + ":" + str(maxX) + "]"

    def get_yrange(self, margin=1):
        '''Get vertical range for which graph will be displayed extanded by margin on both side'''
        minY = None
        maxY = None
        for p in self.points:
            if minY == None:
                minY = p.y
                maxY = p.y
            else:
                minY = min(minY, p.y)
                maxY = max(maxY, p.y)
        return (minY - margin, maxY  + margin)

    def get_gp_yrange(self):
        '''Return yrange for gnuplot script'''
        minY, maxY = self.get_yrange()
        return "[y = " + str(minY) + ":" + str(maxY) + "]"


class Circle(Plot):
    def __init__(self, radius):
        super(Circle, self).__init__()
        self.radius = radius

    def get_point(self, t):
        '''Get Point at angle t on the circle'''
        x = self.radius * math.cos(t)
        y = self.radius * math.sin(t)
        x, y = Point.snap(x, y)
        return Point(x, y)


    def build_points(self):
        '''Build list of points, number of samples is based on minimum step necessary to see the first square'''
        self.points.clear()
        # r.sin(step) = 1
        step = math.asin(1.0 / self.radius)
        t = 0
        while t <= math.pi / 2:
            p = self.get_point(t)
            p2 = p.mirror_y()
            p3 = p.mirror_x()
            p4 = p.mirror_xy()
            self.points.add(p)
            self.points.add(p2)
            self.points.add(p3)
            self.points.add(p4)
            t = t + step

class HalfCircle(Circle):
    def __init__(self, radius):
        super(HalfCircle, self).__init__(radius)
        self.radius = radius

    def build_points_deprecated(self):
        '''Build list of points for the half circle
        iterating over high number of positions'''
        self.points.clear()
        # Number of samples
        samples_number = self.radius * 300
        for i in range(samples_number):
            t = i * math.pi / samples_number
            self.points.add(self.get_point(t))

    def build_points(self):
        '''Build list of points, number of samples is based on minimum step necessary to see the first square'''
        self.points.clear()
        # r.sin(step) = 1
        step = math.asin(1.0 / self.radius)
        t = 0
        while t <= math.pi / 2:
            p = self.get_point(t)
            p2 = p.mirror_y()
            self.points.add(p)
            self.points.add(p2)
            t = t + step

def Ellipsis(Plot):
    def __init__(self, a, b):
        super(Ellipsis, self).__init__()
        self.a = a
        self.b = b

    def build_points(self):
        return


if __name__ == "__main__":

    # Half Circle
    hc = HalfCircle(20)
    hc.build_points()
    hc.offset(263,50)
    hc.gp_script("ocean")

    # Circle
    circle = Circle(30)
    circle.build_points()
    circle.offset(200,222)
    circle.gp_script("circle")



#!/usr/bin/env python
import math
import itertools
import operator
from sets import Set

class Point:
    """
    Point with cartesian coordinates.
    
    Methods prefixed with gp_ are intended to be used for gnuplot plotting.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """Return string representation of Point"""
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        """Two points are equals if their coordinates are equals."""
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Hash function used to adds object of this classes to Set, Dict..."""
        return hash((self.x, self.y))

    def mirror_y(self):
        """Return symetrical point on y axis"""
        return Point(-self.x, self.y)

    def mirror_x(self):
        """Return symetrical point on x axis"""
        return Point(self.x, -self.y)

    def mirror_xy(self):
        """Return symetrical point from origin"""
        return Point(-self.x, -self.y)

    @staticmethod
    def snap(x, y):
        """Snap point to the integer grid"""
        return (round(x), round(y))

    def offset(self, offset_x, offset_y):
        """Apply offset to point"""
        self.x += offset_x
        self.y += offset_y

    def rotate(self, t):
        """Rotate point at an angle t around origin"""
        # Rotation matrix
        m = [[math.cos(t), -math.sin(t)],[math.sin(t), math.cos(t)]]
        v = [self.x, self.y]
        # Apply matrix to point's coordinates
        self.x = sum(itertools.starmap(operator.mul, itertools.izip(v, m[0])))
        self.y = sum(itertools.starmap(operator.mul, itertools.izip(v, m[1])))

    def gp_str(self):
        """Return gnuplot point notation"""
        return str(self.x) + " " + str(self.y) + "\n"

    def gp_dump_boxxy(self):
        """Return point as boxxyerrorbars to draw a box instead of a single dot"""
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
    """List of point with methods to display/dump datas for gnuplot"""
    def __init__(self):
        self.points = list()

    def __str__(self):
        s = ""
        for p in self.points:
            s += str(p) + "\n"
        return s

    def dump(self, output="/dev/stdout"):
        """Dump data to stdout or file if provided"""
        f_out = open(output, "wb")
        for p in self.points:
             f_out.write(p.gp_dump_boxxy())

    def add(self, p):
        """Add Point to list if not already present"""
        if p not in self.points:
            self.points.append(p)

    def gp_script(self, script_name):
        """Generate gnuplot script and dump data to file"""
        data_file = script_name + ".dat"
        # script
        f_out = open(script_name + ".gnu", "wb")
        # make sure x/y axes have same scale
        f_out.write("set size ratio -1\n")
        f_out.write("plot '" + data_file + "' with boxxyerrorbars\n")
        f_out.write("pause -1\n")
        f_out.write("# vim: set syntax=gnuplot:\n")

        # data file
        self.dump(data_file)


    def offset(self, offset_x, offset_y):
        """Apply offset to all the points"""
        # NOTE: we are modifying the elements of the set we are currently iterating
        # I would expecte to have issue because modifying an element changes its hash
        # It looks like it is working though
        for p in self.points:
            p.offset(offset_x, offset_y)

    def get_xrange(self, margin=1):
        """Get horizontal range for which graph will be displayed extanded by margin on both side"""
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
        """Return xrange for gnuplot script"""
        minX, maxX = self.get_xrange()
        return "[x = " + str(minX) + ":" + str(maxX) + "]"

    def get_yrange(self, margin=1):
        """Get vertical range for which graph will be displayed extanded by margin on both side"""
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
        """Return yrange for gnuplot script"""
        minY, maxY = self.get_yrange()
        return "[y = " + str(minY) + ":" + str(maxY) + "]"


class Circle(Plot):
    """List of points to form a circle in a discrete cartesian coordinates system"""
    def __init__(self, radius):
        super(Circle, self).__init__()
        self.radius = radius

    def get_point(self, t):
        """
        Get Point at angle t on the circle
        
        Point is snapped to integer coordinates"""
        x = self.radius * math.cos(t)
        y = self.radius * math.sin(t)
        x, y = Point.snap(x, y)
        return Point(x, y)


    def build_points(self):
        """
        Build list of points.
        
        Number of samples is based on minimum step necessary to see the first square.
        """
        del self.points[:]
        # r.sin(step) = 1
        step = math.asin(1.0 / self.radius)
        t = 0
        while t <= math.pi / 2:
            p = self.get_point(t)
            p2 = p.mirror_y()
            p3 = p.mirror_x()
            p4 = p.mirror_xy()
            self.add(p)
            self.add(p2)
            self.add(p3)
            self.add(p4)
            t = t + step

class HalfCircle(Circle):
    """List of points to form a half circle in a discrete cartesian coordinates system."""
    def __init__(self, radius):
        super(HalfCircle, self).__init__(radius)
        self.radius = radius

    def build_points_deprecated(self):
        """
        Build list of points for the half circle.

        Iterating over high number of positions
        """
        del self.points[:]
        # Number of samples
        samples_number = self.radius * 300
        for i in range(samples_number):
            t = i * math.pi / samples_number
            self.add(self.get_point(t))

    def build_points(self):
        """
        Build list of points.

        Number of samples is based on minimum step necessary to see the first square.
        """
        del self.points[:]
        # r.sin(step) = 1
        step = math.asin(1.0 / self.radius)
        t = 0
        while t <= math.pi / 2:
            p = self.get_point(t)
            p2 = p.mirror_y()
            self.add(p)
            self.add(p2)
            t = t + step

class Ellipse(Plot):
    """List of point to form an ellipse in a disrete cartesian coordinates system."""
    def __init__(self, a, b):
        super(Ellipse, self).__init__()
        self.a = a
        self.b = b

    def get_point(self, t):
        """Get point of ellipse at angle t."""
        # r(t) = a*b / sqrt( (b*cos(t))^2 + (a*sin(t))^2 )
        r = self.a * self.b / math.sqrt(math.pow(self.b * math.cos(t), 2) +
                                        math.pow(self.a * math.sin(t), 2))
        x = r * math.cos(t)
        y = r * math.sin(t)
        x, y = Point.snap(x, y)
        return Point(x, y)


    def build_points(self):
        """Build list of points of ellipse."""
        # max(a,b) * sin(step) = 1
        step = math.asin(1.0 / max(self.a, self.b))
        t = 0
        while t < math.pi/2:
            p = self.get_point(t)
            p2 = p.mirror_y()
            p3 = p.mirror_x()
            p4 = p.mirror_xy()
            self.add(p)
            self.add(p2)
            self.add(p3)
            self.add(p4)
            t += step


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

    # Ellipse
    ellipse = Ellipse(10, 5)
    ellipse.build_points()
    ellipse.gp_script("ellipse")


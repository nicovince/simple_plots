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


class Plot(object):
    '''Plot object is a list of point with methods to display/dump datas'''
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
             f_out.write(str(p) + "\n")

    def offset(self, offset_x, offset_y):
        '''Apply offset to all the points'''
        # NOTE: we are modifying the elements of the set we are currently iterating
        # I would expecte to have issue because modifying an element changes its hash
        # It looks like it is working though
        for p in self.points:
            p.offset(offset_x, offset_y)


class HalfCircle(Plot):
    def __init__(self, radius):
        super(HalfCircle, self).__init__()
        self.radius = radius

    def build_points(self):
        '''Build list of points for the half circle'''
        self.points.clear()
        # Number of samples
        samples_number = self.radius * 300
        for i in range(samples_number):
            t = i * math.pi / samples_number
            self.points.add(self.get_point(t))

    def build_points_step(self):
        '''Build list of points, number of samples is based on minimum step necessary to see the first square'''
        self.points.clear()
        #r.sin(step) = 1
        step = math.asin(1.0 / self.radius)
        print "step : " + str(step)
        t = 0
        while t <= math.pi / 2:
            p = self.get_point(t)
            p2 = p.mirror_y()
            self.points.add(p)
            self.points.add(p2)
            t = t + step
    
    def get_point(self, t):
        '''Get Point at angle t on the half circle'''
        x = self.radius * math.cos(t)
        y = self.radius * math.sin(t)
        x, y = Point.snap(x, y)
        return Point(x, y)

if __name__ == "__main__":
    hc = HalfCircle(10)
    hc.build_points()
    print "Number of points with build_points : " + str(len(hc.points))
    #hc.dump()
    hc.build_points_step()
    print "Number of points with build_points_step : " + str(len(hc.points))
    hc.dump("center.txt")
    hc.offset(100,100)
    hc.dump("offset.txt")

    plot = Plot()
    plot.points.add(Point(0,0))
    plot.points.add(Point(1,0))
    print plot
    for p in plot.points:
        p.offset(-1,0)
        break
    print plot
    plot.points.discard(Point(0,0))
    print plot


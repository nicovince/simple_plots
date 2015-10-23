#!/usr/bin/env python
import math
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

    @staticmethod
    def snap(x, y):
        '''Snap point to the integer grid'''
        return (round(x), round(y))

class HalfCircle:
    def __init__(self, radius):
        self.radius = radius
        self.points = Set()

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
        #r.sin(step/2) = 1
        step = math.asin(1.0 / self.radius)
        print "step : " + str(step)
        t = 0
        while t <= math.pi:
            self.points.add(self.get_point(t))
            t = t + step
    
    def get_point(self, t):
        '''Get Point at angle t on the half circle'''
        x = self.radius * math.cos(t)
        y = self.radius * math.sin(t)
        x, y = Point.snap(x, y)
        return Point(x, y)

    def dump(self, output="/dev/stdout"):
        f_out = open(output, "wb")
        for p in self.points:
             f_out.write(str(p) + "\n")

if __name__ == "__main__":
    hc = HalfCircle(10)
    hc.build_points()
    print "Number of points with build_points : " + str(len(hc.points))
    hc.dump("1.txt")
    hc.build_points_step()
    print "Number of points with build_points_step : " + str(len(hc.points))
    hc.dump("2.txt")

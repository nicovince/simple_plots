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
        self.build_points()

    def build_points(self):
        '''Build list of points for the half circle'''
        # Number of samples
        samples_number = self.radius * 3
        for i in range(samples_number):
            t = i * math.pi / samples_number
            self.points.add(self.get_point(t))
    
    def get_point(self, t):
        '''Get Point at angle t on the half circle'''
        x = self.radius * math.cos(t)
        y = self.radius * math.sin(t)
        x, y = Point.snap(x, y)
        return Point(x, y)


if __name__ == "__main__":
    hc = HalfCircle(10)
    for p in hc.points:
        print p

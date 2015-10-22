#!/usr/bin/env python
import math

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

class HalfCircle:
    def __init__(self, radius):
        self.radius = radius
        self.points = []
        self.build_points()

    def build_points(self):
        '''Build list of points for the half circle'''
        for i in range(self.radius*2):
            t = i * math.pi / (self.radius * 2)
            self.add_point(self.get_point(t))
    
    def get_point(self, t):
        '''Get Point at angle t on the half circle'''
        x = self.radius * math.cos(t)
        y = self.radius * math.sin(t)
        return Point(x, y)

    def add_point(self, p):
        '''Add point to the list if it is not already present'''
        if p not in self.points:
            self.points.append(p)


if __name__ == "__main__":
    print "hello"
    p = Point(3, 4)
    print p
    hc = HalfCircle(10)
    for p in hc.points:
        print p

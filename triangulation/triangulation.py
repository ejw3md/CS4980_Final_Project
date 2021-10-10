from scipy.optimize import fsolve
import sys
from math import exp, sqrt


# data that I got to work:: should output (2, 2) -> python3 triangulation.py 2.828 2.236 2.236 0 1 0 0 0 1 .5 .25 .5 .75
C = 343
#TODO: add C to equations
def equations(x0, pos1, pos2, t1, t2, t3):
    t_ab = t2 - t1
    t_ac = t3 - t1

    xb, yb = pos1
    xc, yc = pos2

    x, y = x0
    eq1 = sqrt( (x-xb)**2 + (y - yb)**2 ) - sqrt(x**2 + y**2) - t_ab
    eq2 = sqrt( (x-xc)**2 + (y - yc)**2 ) - sqrt(x**2 + y**2) - t_ac
    return [eq1, eq2]

def convert_to_xy(lat1, long1):
    #TODO: conversion
    return lat1, long1

def get_best_guess(pos1, vec1, pos2, vec2):
    line1 = [pos1, (vec1[0] + pos1[0], vec1[1] + pos1[1])]
    line2 = [pos2, (vec2[0] + pos2[0], vec2[1] + pos2[1])]

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       print("Lines do not intersect", file=sys.stderr)
       exit(1)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def main():
    if len(sys.argv) != 14:
        print('Invalid number of arguments!', file=sys.stderr)
        exit(1)

    # get input variables
    t1 = float(sys.argv[1])
    t2 = float(sys.argv[2])
    t3 = float(sys.argv[3])
    lat1 = float(sys.argv[4])
    lat2 = float(sys.argv[5])
    lat3 = float(sys.argv[6])
    long1 = float(sys.argv[7])
    long2 = float(sys.argv[8])
    long3 = float(sys.argv[9])
    vec1x = float(sys.argv[10])
    vec2x = float(sys.argv[11])
    vec1y = float(sys.argv[12])
    vec2y = float(sys.argv[13])

    # convert from lat long to xy
    pos1 = convert_to_xy(lat1, long1)
    pos2 = convert_to_xy(lat2, long2)
    pos3 = convert_to_xy(lat3, long3)
    
    # make pos1 at (0, 0)
    offset = pos1
    pos1 = (pos1[0] - offset[0], pos1[1] - offset[1])
    pos2 = (pos2[0] - offset[0], pos2[1] - offset[1])
    pos3 = (pos3[0] - offset[0], pos3[1] - offset[1])

    # get best guess for point
    vec1 = [vec1x, vec1y]
    vec2 = [vec2x, vec2y]
    best_guess = get_best_guess(pos1, vec1, pos2, vec2)

    # solve numerically using best guess
    x, y =  fsolve(equations, best_guess, (pos2, pos3, t1, t2, t3))
    x += offset[0]
    y += offset[1]
    print(x, y)


if __name__ == '__main__':
    main()

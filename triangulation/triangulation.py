from scipy.optimize import fsolve
import sys
from math import exp, sqrt, cos, sin, asin, atan2


# TODO: test longitude and lattitude conversions
C = 343
EARTH_RADIUS = 6371000

def equations(x0, pos1, pos2, pos3):
    # grab all input parameters
    x1, y1, t1 = pos1
    x2, y2, t2 = pos2
    x3, y3, t3 = pos3

    # get values from vector
    x, y, t = x0

    # set up equations we are solving
    eq1 = sqrt( (x-x1)**2 + (y - y1)**2 ) - C * ( t1 - t )
    eq2 = sqrt( (x-x2)**2 + (y - y2)**2 ) - C * ( t2 - t )
    eq3 = sqrt( (x-x3)**2 + (y - y3)**2 ) - C * ( t3 - t )

    return [eq1, eq2, eq3]

def convert_to_xy(lat, long):
    # x and y coordinates
    x = EARTH_RADIUS * cos(lat) * cos(long)
    y = EARTH_RADIUS * cos(lat) * sin(long)

    # return the tuple
    return x, y

def convert_to_lat_long(x, y, device_lat):
    z  = EARTH_RADIUS * sin(device_lat)
    lat = asin(z / EARTH_RADIUS)
    long = atan2(y, x)

    return lat, long

def get_best_guess(pos1, pos2, pos3):
    # our best guess is mic with smallest time
    t1 = pos1[2]
    t2 = pos2[2]
    t3 = pos3[2]

    if t1 < t2 and t1 < t3:
        return (pos1[0], pos1[1], 0)
    elif t2 < t1 and t2 < t3:
        return (pos2[0], pos2[1], 0)
    else:
        return (pos3[0], pos3[1], 0)

def main():
    if len(sys.argv) != 10:
        print('Invalid number of arguments!', file=sys.stderr)
        exit(1)

    # get input variables
    times = [float(x) for x in sys.argv[1:4]]
    lats = [float(x) for x in sys.argv[4:7]]
    longs = [float(x) for x in sys.argv[7:10]]

    # convert from lat long to xy
    pos1 = convert_to_xy(lats[0], longs[0])
    pos2 = convert_to_xy(lats[1], longs[1])
    pos3 = convert_to_xy(lats[2], longs[2])

    # make pos1 at (0, 0)
    offset = pos1
    pos1 = (pos1[0] - offset[0], pos1[1] - offset[1], times[0])
    pos2 = (pos2[0] - offset[0], pos2[1] - offset[1], times[1])
    pos3 = (pos3[0] - offset[0], pos3[1] - offset[1], times[2])

    # get best guess for point
    best_guess = get_best_guess(pos1, pos2, pos3)

    # solve numerically using best guess (Newton-Raphson method)
    x, y, t = fsolve(equations, best_guess, (pos1, pos2, pos3))
    x += offset[0]
    y += offset[1]

    # convert back from x, y coordinates to lat, long
    lat, long = convert_to_lat_long(x, y, lats[0])

    # print the answer
    print(lat, long)


if __name__ == '__main__':
    main()

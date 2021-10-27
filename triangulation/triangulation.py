from scipy.optimize import fsolve
import numpy as np
import sys
from math import cos, sin, asin, atan2

# data that I got to work:: should output (2, 2) -> python3 triangulation.py 2.828 2.236 2.236 0 1 0 0 0 1 .5 .25 .5 .75
C = 343
EARTH_RADIUS = 6371000

def get_sound_loc(pos1, pos2, t_origin, t1, t2):
    x1, y1 = pos1
    x2, y2 = pos2

    # set up the matrix multiplication
    lhs = np.array([[-2 * x1, -2 * y1], [-2 * x2, -2 * y2]], dtype=np.float64)

    ans1 = -x1**2 - y1**2 + t1**2 - t_origin**2
    ans2 = -x2**2 - y2**2 + t2**2 - t_origin**2

    rhs = np.array([[ans1], [ans2]], dtype=np.float64)

    # do matrix multiplication to compute the answer
    res = np.dot(np.linalg.inv(lhs), rhs)

    # return x, y
    return res[0][0], res[1][0]

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

    # solve triangulation to get position of object
    x, y = get_sound_loc(pos2, pos3, t1, t2, t3)

    x += offset[0]
    y += offset[1]

    lat, long = convert_to_lat_long(x, y, lat1)
    print(lat, long)


if __name__ == '__main__':
    main()

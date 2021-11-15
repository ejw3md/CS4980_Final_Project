############################################################
#   TRIANGULATION SCRIPT
#
#   The purpose of this module is to compute the lat long
#   coordinates of the sound given 3 positions of 
#   the microphones that heard the sound, and the times
#   the microphones heard the sound.
#
#   Input:
#       3 microphone lattitude longitude coordinates
#       3 times
#
#   Output:
#       lat and long of triangulated sound
#
#
############################################################

from scipy.optimize import fsolve
import sys
from math import sqrt, cos, radians, degrees

'''
############################################################
TEST COMMAND - data obtained with google maps


python3 triangulation.py \
0.03796226239 0.02611682798 0.02172699708 \
38.97623917161576 38.97628921549201 38.97614586018865 \
-92.25761003060849 -92.25743300461887 -92.25744574549879

Should output something close to: 
    38.97621310689329, -92.25746183858462
############################################################
'''
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

def convert_to_xy(lat, long, center_lat):
    # convert lat long to radians to make computations easier
    lat = radians(lat)
    long = radians(long)
    center_lat = radians(center_lat)

    # compute a equirectangular projection to get x and y
    x = EARTH_RADIUS * long * cos(center_lat)
    y = EARTH_RADIUS * lat

    # return the tuple
    return x, y

def convert_to_lat_long(x, y, center_lat):
    # make sure center is in radians
    center_lat = radians(center_lat)

    # do a reverse equirectangular projection
    long = x / (EARTH_RADIUS * cos(center_lat))
    lat = y / EARTH_RADIUS

    # convert from radians to degrees
    long = degrees(long)
    lat = degrees(lat)

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

def get_sound_coordinates(mic1, mic2, mic3):
    center_lat = (mic1['lat'] + mic2['lat'] + mic3['lat']) / 3

    # convert from lat long to xy
    pos1 = convert_to_xy(mic1['lat'], mic1['long'], center_lat) + (mic1['time'],)
    pos2 = convert_to_xy(mic2['lat'], mic2['long'], center_lat) + (mic2['time'],)
    pos3 = convert_to_xy(mic3['lat'], mic3['long'], center_lat) + (mic3['time'],)

    # get best guess for point
    best_guess = get_best_guess(pos1, pos2, pos3)

    # solve numerically using best guess (Newton-Raphson method)
    x, y, t = fsolve(equations, best_guess, (pos1, pos2, pos3))

    # convert back from x, y coordinates to lat, long
    lat, long = convert_to_lat_long(x, y, center_lat)

    # print the answer
    print(lat, long)


if __name__ == '__main__':
    # this is for running tests of triangulation.py module

    if len(sys.argv) != 10:
        print('Invalid number of arguments!', file=sys.stderr)
        exit(1)

    # get input variables
    times = [float(x) for x in sys.argv[1:4]]
    lats = [float(x) for x in sys.argv[4:7]]
    longs = [float(x) for x in sys.argv[7:10]]

    mics = []
    for time, lat, long in zip(times, lats, longs):
        mics.append({'time': time, 'lat': lat, 'long': long})
    get_sound_coordinates(mics[0], mics[1], mics[2])

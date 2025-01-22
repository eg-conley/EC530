# assignment 1: if user gives two arrays of geo locations, match each point in first array to closest in the second array

# idea: iterate through first array once, applying havertine formula to every point on second
# find min value of the new array and store in map of sorts with first location
# error checking: latitude bw -90 and 90 degrees, longitude bw -180 and 180 degrees
#                 if two distances are equal
#                 other formats of geo location input


# references: https://louwersj.medium.com/calculate-geographic-distances-in-python-with-the-haversine-method-ed99b41ff04b for haversine
#             https://www.latlong.net for distance verification

import math

# sub-task 1: distance between two given points in form of [latitude, longitude]
def dist_two_points(loc1, loc2):
    # convert to radians
    lat1 = math.radians(loc1[0])
    lon1 = math.radians(loc1[1])
    lat2 = math.radians(loc2[0])
    lon2 = math.radians(loc2[1])

    # find diff in latitude and longitude
    latDiff = lat2 - lat1
    lonDiff = lon2 - lon1

    # Haversine formula - shortest distance between two points on a sphere
    a = math.pow(math.sin(latDiff/2),2) + math.cos(lat1) *  math.cos(lat2) * math.pow(math.sin(lonDiff/2),2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371 # km

    # distance formula where R is radius of Earth
    return r * c

def tests():
    print('Testing')
    # subtest 1 cases
    Boston = [42.3555, -71.0565]
    Chicago = [41.8781, -87.6298]
    print('Boston to Chicago: ', round(dist_two_points(Boston, Chicago),4), 'km')

tests()
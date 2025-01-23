# assignment 1: if user gives two arrays of geo locations, match each point in first array to closest in the second array
# using this class to also learn python so if it is rough looking code, pls forgive

# idea: iterate through first array once, applying haversine formula to every point on second
# find min value of the new array and store in map of sorts with first location
# considerations: latitude bw -90 and 90 degrees, longitude bw -180 and 180 degrees
#                 if two distances are equal - solved with min function, just chooses one
#                 other formats of geo location input


# references: https://louwersj.medium.com/calculate-geographic-distances-in-python-with-the-haversine-method-ed99b41ff04b for haversine
#             https://www.latlong.net for distance verification

import math

# sub-task 1: distance between two given points in form of [latitude, longitude]
def dist_two_points(loc1, loc2):
    # error check
    if not (-90 <= loc1[0] <= 90) and (-90 <= loc2[0] <= 90) and (-180 <= loc1[1] <= 180) and (-180 <= loc2[1] <= 180):
        raise ValueError("You have an invalid coordinate")
    else:
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

        # distance formula where R is radius of Earth in km
        return r * c

# not most efficient, but iterating through second array for each element in first
# returns list with [location from array 1],[closest location from array 2]
def dist_all_points(locArray1,locArray2):
    closestLocations = []
    for loc1 in locArray1:
        distances = [dist_two_points(loc1,loc2) for loc2 in locArray2]
        point = distances.index(min(distances))
        closestLocations.append([loc1, locArray2[point]])
    return closestLocations


# software engineering principles

assignment 1: if user gives two arrays of geo locations, match each point in first array to closest in the second array
using this class to also learn python so if it is rough looking code, pls forgive

idea: iterate through first array once, applying haversine formula to every point on second
find min value of the new array and store in map of sorts with first location
considerations: latitude bw -90 and 90 degrees, longitude bw -180 and 180 degrees
                 if two distances are equal - solved with min function, just chooses one
                 other formats of geo location input


references: https://louwersj.medium.com/calculate-geographic-distances-in-python-with-the-haversine-method-ed99b41ff04b for haversine
             https://www.latlong.net for distance verification

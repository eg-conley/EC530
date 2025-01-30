import math
import pandas as pd
import re

# function returns distance between two geo locations in form (latitude, longitude)
def dist_two_points(loc1, loc2):
        # convert to radians
        lat1 = math.radians(loc1[0])
        lon1 = math.radians(loc1[1])
        lat2 = math.radians(loc2[0])
        lon2 = math.radians(loc2[1])

        # find diff in latitude and longitude
        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1

        # Haversine formula - shortest distance between two points on a sphere
        a = math.pow(math.sin(lat_diff/2),2) + math.cos(lat1) *  math.cos(lat2) * math.pow(math.sin(lon_diff/2),2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        r = 6371 # km

        # distance formula where R is radius of Earth in km
        return r * c

# not most efficient, but iterating through second array for each element in first
# returns list with [location from array 1],[closest location from array 2]
def dist_all_points(loc1_array, loc2_array):
    closest_locations = []
    for loc1 in loc1_array:
        distances = [dist_two_points(loc1, loc2) for loc2 in loc2_array]
        point = distances.index(min(distances))
        closest_locations.append([loc1, loc2_array[point]])
    return closest_locations

def ddm_to_decimal(point):
    degrees = float(point.split(' ')[0])
    minutes = float(point.split(' ')[1])
    return degrees + (minutes/60)

def dms_to_decimal(point):
    split_point1 = point.split('°')
    split_point2 = split_point1[1].split("'")

    degrees = float(split_point1[0])
    minutes = float(split_point2[0])
    seconds = float(split_point2[1].replace('"', ''))
    return degrees + (minutes / 60) + (seconds / 3600)

def clean_data(coord):
    clean_coord = []
    for point in coord:
        if type(point) == float:
            clean_coord.append(point)
        else:
            try:
                # check for directional characters (N, E, S, W)
                if any(direction in point.upper() for direction in ['N', 'S', 'E', 'W']):
                    if 'S' in point.upper() or 'W' in point.upper():
                        # make negative
                        point = '-' + point

                # check if in ddm form
                if ' ' and '.' in point:
                    point = ddm_to_decimal(point)
                # check if in dms form
                elif '"' in point:
                    point = dms_to_decimal(point)

                # remove non-numbers
                if type(point) != float:
                    point = re.sub('[^0-9.,-]', '', point)

                clean_coord.append(float(point))

            except ValueError as e:
                print(e)
    return tuple(clean_coord)

def main():
    # declare arrays for input data (not cleaned)
    loc1 = []
    loc2 = []

    user_input1 = input('Enter title of first file or press 1 to input manually: ')
    if user_input1 == '1':
            should_continue = 'y'
            while should_continue == 'y':
                lat = input("Latitude: ")
                lon = input("Longitude: ")
                loc1.append( (float(lat),float(lon)) )
                should_continue = input('Do you want to continue? (y/n): ')
    else:
        # read csv into dataframe
        has_header1 = input('Does the file have a header? (y/n): ')
        if has_header1 == 'n':
            user_lat1 = input('Enter number of latitude column (0 index): ')
            user_lon1 = input('Enter number of longitude column (0 index): ')
            df1 = pd.read_csv(user_input1, header=None, usecols=[int(user_lat1), int(user_lon1)])
            loc1 = list(zip(df1[int(user_lat1)], df1[int(user_lon1)]))
        else:
            df1 = pd.read_csv(user_input1)
            user_lat1 = input('Enter name of latitude column: ')
            user_lon1 = input('Enter name of longitude column: ')
            loc1 = list(zip(df1[user_lat1], df1[user_lon1]))

    user_input2 = input('Enter title of second file or press 1 to input manually: ')
    if user_input2 == '1':
        should_continue = 'y'
        while should_continue == 'y':
            lat = input("Latitude: ")
            lon = input("Longitude: ")
            loc2.append( (float(lat),float(lon)) )
            should_continue = input('Do you want to continue? (y/n): ')
    else:
        has_header2 = input('Does the file have a header? (y/n): ')
        if has_header2 == 'n':
            user_lat2 = input('Enter number of latitude column: ')
            user_lon2 = input('Enter number of longitude column: ')
            df2 = pd.read_csv(user_input2, header=None, usecols=[int(user_lat2), int(user_lon2)])
            loc2 = list(zip(df2[int(user_lat2)], df2[int(user_lon2)]))
        else:
            df2 = pd.read_csv(user_input2)
            user_lat2 = input('Enter name of latitude column: ')
            user_lon2 = input('Enter name of longitude column: ')
            loc2 = list(zip(df2[user_lat2], df2[user_lon2]))

    # parse data/error check and make sure it meets correct conventions to be used in the equation
    loc1_clean = []
    loc2_clean = []

    for coord_pair1 in loc1:
        clean_pair1 = clean_data(coord_pair1)
        if clean_pair1 is None:
            print(f"Coordinates {clean_pair1} not valid and will not be used")
        elif not (-90 <= clean_pair1[0] <= 90 and -180 <= clean_pair1[1] <= 180):
            print(f"Coordinates {clean_pair1} not valid and will not be used")
        else:
            loc1_clean.append(clean_pair1)


    for coord_pair2 in loc2:
        clean_pair2 = clean_data(coord_pair2)
        if clean_pair2 is None:
            print(f"Coordinates {clean_pair2} not valid and will not be used")
        elif not (-90 <= clean_pair2[0] <= 90 and -180 <= clean_pair2[1] <= 180):
            print(f"Coordinates {clean_pair2} not valid and will not be used")
        else:
            loc2_clean.append(clean_pair2)

    # create arrays and pass into function
    result = dist_all_points(loc1_clean, loc2_clean)
    print(result)

main()

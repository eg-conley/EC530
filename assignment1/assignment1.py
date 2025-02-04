import math
import pandas as pd
import re
import sys

# this function returns the spherical distance between two geo-locations passed into the function in (latitude, longitude) form
def haversine(location1, location2):
    r = 6371 # define radius of earth in km

    # convert to radians
    lat1 = math.radians(location1[0])
    lon1 = math.radians(location1[1])
    lat2 = math.radians(location2[0])
    lon2 = math.radians(location2[1])

    # find diff in latitude and longitude
    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1

    # Haversine formula finds shortest distance between two points on a sphere
    a = math.pow(math.sin(lat_diff/2),2) + math.cos(lat1) *  math.cos(lat2) * math.pow(math.sin(lon_diff/2),2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # distance formula where R is radius of Earth in km
    return r * c

# this function returns an array with each location in the first array and its closest location from the second array
# not currently the most efficient (n^2)
def match_closest(location_arr1, location_arr2):
    matched = []
    for location1 in location_arr1:
        distances = [haversine(location1, location2) for location2 in location_arr2]
        min_dist_index = distances.index(min(distances))
        matched.append([location1, location_arr2[min_dist_index]])
    return matched

# this function scrubs the location points and makes sure that only those in the form (latitude, longitude) are used
# it accounts for and corrects the data  if N, S, E, W are included
def clean_data(location):
    clean_location = []
    for i, point in enumerate(location):
        # check for directional characters (N, E, S, W)
        if isinstance(point, str):
            point = point.strip().upper() # remove spaces and uppercase if needed
            if 'S' in point or 'W' in point:
                point = re.sub('[^0-9.]', '', point) # remove letter
                point = '-' + point # make negative
            else:
                point = re.sub('[^0-9.-]', '', point) # just remove letter
        try:
            point = float(point)
        except ValueError as e:
            print('Please use locations in the format (latitude, longitude)')
            print(e)
            return None

        # check latitude and longitude bounds
        if i == 0 and not -90 <= point <= 90:
            #print(f"Invalid latitude: {point}. Won't be used.")
            return None
        if i == 1 and not -180 <= point <= 180:
            #print(f"Invalid longitude: {point}. Won't be used.")
            return None

        clean_location.append(point)
    return tuple(clean_location)

# this function loads in data from a csv file and calls the other functions
# user can also elect to manually input values
def main():
    # arrays for csv data
    location_arr1 = []
    location_arr2 = []
    location_arr1_clean = []
    location_arr2_clean = []

    user_input1 = input('Enter title of first file or press 0 to input manually: ')
    if user_input1 == '0':
        continue_flag = 'y'
        while continue_flag == 'y':
            lat1 = input("Latitude: ")
            lon1 = input("Longitude: ")
            location1_clean = clean_data( (lat1,lon1) )
            if location1_clean is not None:
                location_arr1_clean.append(location1_clean)
            continue_flag = input('Do you want to continue? (y/n): ')
    else:
        try:
            # read csv into dataframe
            df1 = pd.read_csv(user_input1)
            lats1 = input('Enter name of latitude column: ')
            lons1 = input('Enter name of longitude column: ')
            location_arr1 = list(zip(df1[lats1], df1[lons1]))

            # clean the csv data
            for location1 in location_arr1:
                location1_clean = clean_data(location1)
                if location1_clean is not None:
                    location_arr1_clean.append(location1_clean)
        except ValueError as e:
            print('Please use locations in the format (latitude, longitude)')
            print(e)
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The file '{user_input1}' was not found. Please check the path and try again.")
            sys.exit(1)

    user_input2 = input('Enter title of second file or press 0 to input manually: ')
    if user_input2 == '0':
        continue_flag = 'y'
        while continue_flag == 'y':
            lat2 = input("Latitude: ")
            lon2 = input("Longitude: ")
            location2_clean = clean_data((lat2, lon2))
            if location2_clean is not None:
                location_arr2_clean.append(location2_clean)
            continue_flag = input('Do you want to continue? (y/n): ')
    else:
        try:
            # read csv into dataframe
            df2 = pd.read_csv(user_input2)
            lats2 = input('Enter name of latitude column: ')
            lons2 = input('Enter name of longitude column: ')
            location_arr2 = list(zip(df2[lats2], df2[lons2]))

            # clean the csv data
            for location2 in location_arr2:
                location2_clean = clean_data(location2)
                if location2_clean is not None:
                    location_arr2_clean.append(location2_clean)
                location_arr2_clean.append(clean_data(location2))
        except ValueError as e:
            print('Please use locations in the format (latitude, longitude)')
            print(e)
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The file '{user_input1}' was not found. Please check the path and try again.")
            sys.exit(1)

    # apply matching function and return results
    result = match_closest(location_arr1_clean, location_arr2_clean)
    print(result) # for error checking
    return result

main()
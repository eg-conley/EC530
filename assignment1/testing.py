import re
def main():
    lat = '43.2243  new 31word E   '

    clean_lat = lat.replace(" ",'')
    clean_lat = re.sub('[^0-9.]', '', clean_lat)
    clean_lat = float(clean_lat) * -1
    print(clean_lat)

    point = '45°11\'1"'
    print(point)
    # degrees = point.split(' ')[0])
    # minutes = point.split(' ')[1]
    # print('degrees', degrees, 'minutes', minutes)

    split_point1 = point.split('°')
    split_point2 = split_point1[1].split("'")
    print(split_point1[0], split_point2[0], split_point2[1].replace('"', ''))

main()
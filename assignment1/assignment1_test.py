from assignment1 import *

def test_dist_two_points():
    boston = [42.3555, -71.0565]
    chicago = [41.8781, -87.6298]
    paris = [48.8566, 2.3522]
    ny = [40.7128, -74.0060]
    saopaolo = [-23.5505, -46.6333]
    sydney = [-33.8688, 151.2093]
    tokyo = [35.6895, 139.6917]

    assert round(dist_two_points(boston, chicago),4) == 1365.8663
    assert round(dist_two_points(paris, ny),4) == 5837.2409
    assert round(dist_two_points(saopaolo, sydney),4) == 13357.2060
    assert round(dist_two_points([0,0], [0,0]), 4) == 0
    assert round(dist_two_points([-90, -180], [90, 180]), 4) == 20015.0868
    assert round(dist_two_points([-91, 0], [0, 0]), 4) == 100000
    assert round(dist_two_points([0, 90], [760, 0]), 4) == 100000
    assert round(dist_two_points([0, 90], [0, -190]), 4) == 100000

    # subtest 2 cases
    arr1 = [[35.6895, 139.6917],[48.8566, 2.3522],[30.0444, 31.2357]] # tokyo, paris, cairo
    arr2 = [[40.7128, -74.0060],[42.3555, -71.0565],[41.8781, -87.6298]] # new york, boston, chicago
    closest1 = dist_all_points(arr1,arr2)
    for loc in closest1:
        print(f'The closest point to {loc[0]} is {loc[1]}')

    arr3 = [[35.6895, 139.6917],[48.8566, 2.3522]]
    arr4 = [[-91,0]]
    closest2 = dist_all_points(arr3,arr4)
    for loc in closest2:
        print(f'The closest point to {loc[0]} is {loc[1]}')
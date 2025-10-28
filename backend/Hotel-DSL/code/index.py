from faasit_runtime import function, FaasitRuntime

import random
import uuid

@function
def hotelSearch(frt: FaasitRuntime):
    _in = frt.input()

    n = _in["n"]
    k = _in["k"]
    query_x = _in["query_x"]
    query_y = _in["query_y"]
    query = (query_x, query_y)

    unique_id = uuid.uuid4()
    random.seed(unique_id)
    points = []
    for _ in range(n):
        point = (
            random.uniform(0, 100),  # x
            random.uniform(0, 100)   # y
        )
        points.append(point)
    
    def euclidean_distance(p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    
    points_with_dist = [
        (point, euclidean_distance(query, point))
        for point in points
    ]
    points_with_dist.sort(key=lambda x: x[1])

    nearest_points = [
        {
            "brand": unique_id,
            "coords": point,
            "value": random.uniform(0, 100) # value
        }
        for point, _ in points_with_dist[:k]
    ]

    return frt.output({
        "points": nearest_points
    })

handler = hotelSearch.export()
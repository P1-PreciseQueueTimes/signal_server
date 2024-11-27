import math

# This function calculates the distance between known points
# Problem is we need known æoints and all either needs consistency in distance to server.
# Or we need to know the distance to the server from each sniffer. Then calculate a new N value for each sniffer. and Tx power value.
def CalculateDistance(rssi, tx_power, n=2):
    return 10 ** ((tx_power - rssi) / (10 * n))



def Trilateration(points):
    x1, y1, d1 = points[0]['x'], points[0]['y'], points[0]['distance']
    x2, y2, d2 = points[1]['x'], points[1]['y'], points[1]['distance']
    x3, y3, d3 = points[2]['x'], points[2]['y'], points[2]['distance']
    A = 2 * (x2 - x1) ; B = 2 * (y2 - y1) 
    C = d1 ** 2 - d2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    D = 2 * (x3 - x2) ; E = 2 * (y3 - y2)
    F = d2 ** 2 - d3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
    # Solve for x and y
    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)
    return x, y 

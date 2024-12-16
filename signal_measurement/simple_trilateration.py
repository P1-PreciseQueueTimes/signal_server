def Trilateration(points,distances):
    x1, y1, d1 = points[0][0], points[0][1], distances[0] #array is 0=x, 1=y
    x2, y2, d2 = points[1][0], points[1][1], distances[1]
    x3, y3, d3 = points[2][0], points[2][1], distances[2]
    A = 2 * (x2 - x1) ; B = 2 * (y2 - y1) 
    C = d1 ** 2 - d2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    D = 2 * (x3 - x2) ; E = 2 * (y3 - y2)
    F = d2 ** 2 - d3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
    # Solve for x and y
    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)
    return x, y 


import numpy as np 
import math

# This function calculates the distance between known points
# Problem is we need known æoints and all either needs consistency in distance to server.
# Or we need to know the distance to the server from each sniffer. Then calculate a new N value for each sniffer. and Tx power value.
def CalculateDistance(rssi, tx_power, n=2):
    return 10 ** ((tx_power - rssi) / (10 * n))

def trilaterate(A):
    #subtracting first and second equations, then simplifying yields the following:
    l1 = 2 * (A[1, 0] - A[0, 0]) # 2*(x2-x1)
    l2 = 2 * (A[1, 1] - A[0, 1]) # 2*(y2-y1)
    l3 = A[0, 2] ** 2 - A[1, 2] ** 2 - A[0, 0] ** 2 + A[1, 0] ** 2 - A[0, 1] ** 2 + A[1, 1] ** 2 # d1^2-d2^2-x1^2+x2^2-y1^2+y2^2
    #same process as above, but for the second and third equations
    l4 = 2 * (A[2, 0] - A[1, 0]) 
    l5 = 2 * (A[2, 1] - A[1, 1]) 
    l6 = A[1, 2] ** 2 - A[2, 2] ** 2 - A[1, 0] ** 2 + A[2, 0] ** 2 - A[1, 1] ** 2 + A[2, 1] ** 2
    #solving the system of equations
    M = np.array([[l1, l2], 
                  [l4, l5]])
    b = np.array([l3, l6])[:, np.newaxis]
    return np.linalg.solve(M, b) 

def LSM_sol(points): 
    pass

def PCA_sol(points):
    pass


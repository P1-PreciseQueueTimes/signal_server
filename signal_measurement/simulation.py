import random

def loop(error_margin):
    cumerror=0
    for _ in range(10):

        cumerror+=simulate_one_point(random.randint(1,10),random.randint(1,10),error_margin)
    return cumerror
def simulate_one_point(x,y,error_margin):
    Trilateration()
    error=0.4
    return error



def triangulate():
    return 3,3

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

#loop(1)
import numpy as np
from scipy.optimize import minimize
import math
#distances = np.array([5.1, 5.0, 3.1])




def lns(distances):
    """takes 3 positions in that are arrays and an array with the distances"""
    locations = np.array([
            [50, 50],  # P1
            [200, 400],  # P2
            [250, 150]   # P3
    ])
    initial_guess = np.mean(locations, axis=0)
    calculateLNS(locations, distances, initial_guess)

def euclidean_distance(x1, y1, x2, y2):
    p1 = np.array((x1 ,y1))
    p2 = np.array((x2, y2))
    return np.linalg.norm(p1 - p2)

def mse(x, locations, distances): #Funktion that calculates errors/squares
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = euclidean_distance(x[0], x[1], location[0], location[1])
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(distances)

def calculateLNS(locations, distances, initial_guess):
    result = minimize(
        mse,                         # The error function
        initial_guess,            # The initial guess
        args=(locations, distances), # Additional parameters for mse
        method='L-BFGS-B',           # The optimisation algorithm
        options={
            'ftol':1e-5,         # Tolerance
            'maxiter': 1e+7      # Maximum iterations
        })
    location = result.x
    print(f"\nX:{location[0]}\nY:{location[1]}\n")

def calc_distance_reg(rssi):
    return math.exp(-0.1339046599*rssi+ 2.363818961)

lns(np.array([100, 300, 200]))

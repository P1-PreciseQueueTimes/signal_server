import numpy as np
from scipy.optimize import minimize
import math
#distances = np.array([5.1, 5.0, 3.1])

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

def lns(locations,distances):
    """takes 3 positions in that are arrays and an array with the distances"""
    locations = np.array(locations)
    initial_guess = np.mean(locations, axis=0)
    return calculateLNS(locations, distances, initial_guess)


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

    return location

def calc_distance_reg(rssi):
    return math.exp(-0.1339046599*rssi+ 2.363818961)

#lns(1,2,3,np.array([5.1, 5.0, 3.1]))

"""
distances = np.array([5.1, 5.0, 3.1])
locations = np.array([
        [0, 0],  # P1
        [6, 0],  # P2
        [3, 7]   # P3
])    
"""

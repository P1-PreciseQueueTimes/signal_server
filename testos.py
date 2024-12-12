import numpy as np
from scipy.optimize import minimize

def trilaterate(anchors, distances):
    """
    Perform trilateration using mean squared error.

    Args:
        anchors (list of tuples): List of (x, y) coordinates for the anchors.
        distances (list of floats): List of distances to the target from each anchor.

    Returns:
        tuple: Estimated (x, y) coordinates of the target.
    """
    def mse(x):
        """Calculate mean squared error for a given point x."""
        errors = [(np.sqrt((x[0] - ax)**2 + (x[1] - ay)**2) - d)**2 for (ax, ay), d in zip(anchors, distances)]
        return np.mean(errors)

    # Initial guess: centroid of the anchors
    initial_guess = np.mean(anchors, axis=0)

    # Minimize the mean squared error
    result = minimize(mse, initial_guess, method='L-BFGS-B')

    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed: " + result.message)

# Example usage
if __name__ == "__main__":
    # Anchor points (x, y)
    anchors = [(0, 0), (1200, 0), (600, 1200)]

    # Distances from each anchor to the target
    #distances = [780.76, 1096.09, 560.92]

    distances = [780.76, 560.92,1096.09]

    # Perform trilateration
    try:
        target = trilaterate(anchors, distances)
        print(f"Estimated target location: {target}")
    except ValueError as e:
        print(e)


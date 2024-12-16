import misc_elements
from flask import request
def handleRide():
    """
    Changes chosen ride to what is chosen on the website.
    """
    request_data = request.get_json()
    chosen_ride = request_data["value"]
    print(chosen_ride)
    misc_elements.chosen_ride = chosen_ride
    return ""

import misc_elements
import json

def handleRides():
    """
    Handles whenever the html page requests for a list of rides.
    """
    out_obj = {"chosen_ride":misc_elements.chosen_ride,"rides":[ride.name for ride in misc_elements.rides]}
    return json.dumps(out_obj) 

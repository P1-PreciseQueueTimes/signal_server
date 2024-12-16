import misc_elements
import math
def handleESP32():
    """
    Handles whenever esp32 ask for ride time.
    Returns amount of people inserted into a function used the calculate queue time for chosen ride. 
    """
    global will_req_num, will_list
    chosen_ride = None 

    for ride in misc_elements.rides:
        if ride.name == misc_elements.chosen_ride:
            chosen_ride = ride

    if not chosen_ride:
        return "Ride does not exist"


    queue_time = chosen_ride.calculate_queue_time(misc_elements.People_In_Area)

    return f"Ride:{chosen_ride.name}\nMinutes: {math.ceil(queue_time)}"

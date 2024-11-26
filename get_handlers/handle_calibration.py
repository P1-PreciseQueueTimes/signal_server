from misc_elements import RECEIVERS

def handleCalibration(host_name): 

    difference_in_times = RECEIVERS[host_name]

    average_difference = sum(difference_in_times)/len(difference_in_times)

    return str(average_difference) 

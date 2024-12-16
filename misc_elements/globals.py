
from classes import Receiver, Ride


#Name of the fingerprint database.
FINGERPRINT_DB = "fingerprint_db.json"

#Calculates center of circle.
CENTER = (1200/2,1200/2)  

#Initialize receivers.
RECEIVERS =  [Receiver("pie2",[0,0]),Receiver("pie3",[1200,0]),Receiver("pie4",[600,1200])] 

#Current fingerprint location.
Test_x = 0 
Test_y = 0

#List of differences in cordinates between real and calculated.
Tri_x_diff =[] 
Tri_y_diff =[] 

#CALIBRATION_MODE for fingerprinting.
CALIBRATION_MODE = True 

#How many people are in the masuring area.
People_In_Area = 6

# Defining our Rides with their data so we can calculate Flow Rate
rides = [
    Ride(name="Dragekongen", wait_time_minutes=3.5, people_per_ride=28),
    Ride(name="Piraten", wait_time_minutes=2.341463415, people_per_ride=32), 
    Ride(name="Skatteøen", wait_time_minutes=3, people_per_ride=32)
]

#Name of the chosen ride.
chosen_ride = "Piraten"



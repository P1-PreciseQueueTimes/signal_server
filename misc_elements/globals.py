
from classes import Receiver, Ride



FINGERPRINT_DB = "fingerprint_db.json"

CENTER = (1200/2,1200/2)  

RECEIVERS =  [Receiver("pie2",[0,0]),Receiver("pie3",[1200,0]),Receiver("pie4",[600,1200])] 

Test_x = 0 

Test_y = 0

Tri_x_diff =[] 

Tri_y_diff =[] 

CALIBRATION_MODE = True 

People_In_Area = 0

# Defining our Rides with their data so we can calculate Flow Rate
rides = [
    Ride(name="Dragekongen", wait_time_minutes=3.5, people_per_ride=28),
    Ride(name="Piraten", wait_time_minutes=2.31, people_per_ride=2.341463415), 
    Ride(name="Skatteøen", wait_time_minutes=3, people_per_ride=32)
]

chosen_ride = "Piraten"



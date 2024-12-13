# Comment for Martin
class Ride:
    def __init__(self, name, wait_time_minutes, people_per_ride):
        """
        Initialize the Ride object.
        :param name: Name of the ride
        :param wait_time_minutes: Time for one cycle of the ride in minutes
        :param people_per_ride: Number of people accommodated in one run
        """
        self.name = name
        self.wait_time_minutes = wait_time_minutes
        self.people_per_ride = people_per_ride
        self.hourly_capacity = self.calculate_hourly_capacity()
    
    def calculate_hourly_capacity(self):
        """
        Calculate the hourly capacity using the formula made up from 1 Datapoint:
        (60 / wait_time_minutes) * people_per_ride
        """
        return (60 / self.wait_time_minutes) * self.people_per_ride

    def calculate_queue_time(self, people_in_queue):
        """
        Calculate Total wait in minutes for a given queue including bugfer.
        :param People_in_queue: Amount of people in the line
        :return: Total wait time in minutes
        """
        queue_time = (people_in_queue / self.hourly_capacity) * 60  # Convert back to minutes
        return queue_time + 2  # Buffer time in minutes

# Defining our Rides with their data so we can calculate Flow Rate
rides = [
    Ride(name="Dragekongen", wait_time_minutes=3.5, people_per_ride=28),
    Ride(name="Piraten", wait_time_minutes=2.341463415, people_per_ride=32), 
    Ride(name="Skatteøen", wait_time_minutes=3, people_per_ride=32)
]

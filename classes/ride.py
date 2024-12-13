class Ride:
    def __init__(self,flowrate):
        self.flowrate=flowrate

    def calculate_queue_time(self,amount_people):
        return amount_people/self.flowrate

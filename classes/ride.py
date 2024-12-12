class Ride:
    def __init__(self,flowrate):
        self.flowrate=flowrate

    def calculate_queue_time(self,amount_people):
        return amount_people/self.flowrate
    
    #piraten er 16 personer, ridecycle 72seconds, realisticly 80-90.
#øsnkeøen er 8 personer, 2 min/140 sec per tur.



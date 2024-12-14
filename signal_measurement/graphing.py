import numpy as np
import math
#not yet numbers at 600:400 and 300:200

class Vector:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))


class Points:
    def __init__(self,position,position_RSSI_dict):
        self.position=position
        self.RSSI_dict=position_RSSI_dict
        self.dist_RSSI=[]


pi2=Points(Vector(600,1200),{Vector(600,400):[-25,-27,-27,-31,-31,-27,-31,-28,-29,-27,-27,-27,-25,-30,-47,-28,-33,-32,-32,-33,-32,-47,-39,-36,-44,-37,-36],
Vector(300,200):[-47,-36,-39,-58,-36,-36],Vector(1000,400):[-29],
Vector(1400,400):[-51,-47,-40,-44,-45,-31,-34,-36,-44,-39,-37,-54,-44,-48,-45,-38,-41],
Vector(200,600):[-36,-38,-38,-38,-36,-33,-36,-36,-49,-43,-44,-40,-47,-52,-46,-37,-38,-37,-36,-36,-52,-36,-36],
Vector(600,100):[-58,-36,-51,-44,-46,-32,-36,-40,-36,-39]})#spids af trekant
pi3=Points(Vector(0,0),{Vector(600,400):[-70,-27,-31,-31,-25,-32,-36,-31,-28,-28,-35,-34,-65,-28,-31,-34,-34,-38,-61,-36,-32,-52,-28,-34,-31,-35,-58],
Vector(300,200):[-25,-41,-36,-27,-24,-31],Vector(1000,400):[-31],
Vector(1400,400):[-34,-44,-32,-32,-34,-38,-36,-34,-43,-44,-45,-36,-38,-38,-39,-38,-58],
Vector(200,600):[-25,-25,-71,-23,-20,-31,-27,-27,-31,-33,-27,-21,-27,-21,-23,-27,-28,-27,-25,-25,-23,-25,-18],
Vector(600,100):[-34,-29,-27,-31,-27,-24,-31,-28,-28,-27]})
pi4=Points(Vector(1200,0),{Vector(600,400):[-34,-28,-24,-48,-31,-25,-27,-25,-36,-26,-26,-31,-33,-36,-39,-31,-29,-31,-37,-32,-31,-23,-25,-58,-58,-66,-41],
Vector(300,200):[-23,-23,-23,-58,-24,-32],Vector(1000,400):[-28],
Vector(1400,400):[-25,-20,-24,-66,-17,-27,-58,-21,-22,-31,-25,-47,-58,-34,-27,-25,-25],
Vector(200,600):[-23,-31,-36,-35,-58,-58,-58,-36,-33,-34,-34,-41,-32,-51,-35,-27,-31,-41,-31,-71,-47,-44,-44],
Vector(600,100):[-58,-34,-31,-47,-32,-64,-34,-22,-58,-44]})

#loc_val_dict={}
loc_val_list=[Vector(600,400),Vector(300,200),Vector(1000,400),Vector(1400,400),Vector(200,600),Vector(600,100)]

def calc_range(vect1,vect2):
    xdiff=vect1.x-vect2.x
    ydiff=vect1.y-vect2.y
    return math.sqrt(xdiff**2+ydiff**2)

print(pi2.RSSI_dict[Vector(600,400)])


#testloc=3,4
pi1=Vector(2,5)

print(pi1.x)
print(pi1.y)
def distance_RSSI_list():
    for point in loc_val_list: #runs through every sender_location
        distancee=calc_range(point,pi2.position) #calculates distance from sender location and pi
        for RSSIi in pi2.RSSI_dict[point]:#runs through every RSSI value of the pie at the current sender location
            pi2.dist_RSSI.append([distancee,RSSIi])

            
    return

distance_RSSI_list()
print(pi2.dist_RSSI[2])

def graph():
    return

print(calc_range(Vector(0,0),Vector(2,2)))

def calc_distance_reg(rssi):
    return math.exp(-0.1339046599*rssi+ 2.363818961)
    
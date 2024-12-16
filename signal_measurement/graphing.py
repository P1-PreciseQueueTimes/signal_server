import matplotlib.pyplot as plt
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
        self.RSSI_dict=position_RSSI_dict#position as key, RSSI-list as value
        self.dist_RSSI=[]

"""
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
"""
"""
pi2=Points(Vector(600,1200),{Vector(600,400):[-25,-27,-27,-31,-31,-27,-31,-28,-29,-27,-27,-27,-25,-30,-28,-33,-32,-32,-33,-32,-39,-36,-37,-36],
Vector(300,200):[-47,-36,-39,-58,-36,-36],Vector(1000,400):[-29],
Vector(1400,400):[-51,-47,-40,-44,-45,-31,-34,-36,-44,-39,-37,-54,-44,-48,-45,-38,-41],
Vector(200,600):[-36,-38,-38,-38,-36,-33,-36,-36,-49,-43,-44,-40,-47,-46,-37,-38,-37,-36,-36,-52,-36,-36],
Vector(600,100):[-58,-36,-51,-44,-46,-32,-36,-40,-36,-39]})#spids af trekant
pi3=Points(Vector(0,0),{Vector(600,400):[-27,-31,-31,-25,-32,-36,-31,-28,-28,-35,-34,-28,-31,-34,-34,-38,-36,-32,-28,-34,-31,-35],
Vector(300,200):[-25,-41,-36,-27,-24,-31],Vector(1000,400):[-31],
Vector(1400,400):[-34,-44,-32,-32,-34,-38,-36,-34,-36,-38,-38,-39,-38],
Vector(200,600):[-25,-25,-23,-20,-31,-27,-27,-31,-33,-27,-21,-27,-21,-23,-27,-28,-27,-25,-25,-23,-25,-18],
Vector(600,100):[-34,-29,-27,-31,-27,-24,-31,-28,-28,-27]})
pi4=Points(Vector(1200,0),{Vector(600,400):[-34,-28,-24,-31,-25,-27,-25,-36,-26,-26,-31,-33,-36,-39,-31,-29,-31,-37,-32,-31,-23,-25],
Vector(300,200):[-23,-23,-23,-24,-32],Vector(1000,400):[-28],
Vector(1400,400):[-25,-20,-24,-17,-27,-21,-22,-31,-25,-34,-27,-25,-25],
Vector(200,600):[-23,-31,-36,-35,-36,-33,-34,-34,-32,-35,-27,-31,-31],
Vector(600,100):[-34,-31,-32,-34,-22,]})
"""
pi2=Points(Vector(600,1200),{Vector(600,400):[-25,-27,-27,-31,-31,-27,-31,-28,-29,-27,-27,-27,-25,-30,-28,-33,-32,-32,-33,-32,-39,-36,-37,-36],
Vector(300,200):[-36,-39,-36,-36],Vector(1000,400):[-29],
Vector(1400,400):[-51,-47,-40,-44,-45,-31,-34,-36,-44,-39,-37,-54,-44,-48,-45,-38,-41],
Vector(200,600):[-36,-38,-38,-38,-36,-33,-36,-36,-49,-43,-44,-40,-47,-46,-37,-38,-37,-36,-36,-52,-36,-36],
Vector(600,100):[-36,-44,-46,-32,-36,-40,-36,-39]})#spids af trekant
pi3=Points(Vector(0,0),{Vector(600,400):[-27,-31,-31,-25,-32,-36,-31,-28,-28,-35,-34,-28,-31,-34,-34,-38,-36,-32,-28,-34,-31,-35],
Vector(300,200):[-25,-27,-24],Vector(1000,400):[-31],
Vector(1400,400):[-34,-44,-32,-32,-34,-38,-36,-34,-36,-38,-38,-39,-38],
Vector(200,600):[-25,-25,-23,-20,-31,-27,-27,-31,-33,-27,-21,-27,-21,-23,-27,-28,-27,-25,-25,-23,-25,-18],
Vector(600,100):[-34,-29,-27,-31,-27,-24,-31,-28,-28,-27]})
pi4=Points(Vector(1200,0),{Vector(600,400):[-34,-28,-24,-31,-25,-27,-25,-36,-26,-26,-31,-33,-36,-39,-31,-29,-31,-37,-32,-31,-23,-25],
Vector(300,200):[-23,-23,-23,-24,-32],Vector(1000,400):[-28],
Vector(1400,400):[-25,-20,-24,-27,-21,-22,-31,-25,-34,-27,-25,-25],
Vector(200,600):[-31,-36,-35,-36,-33,-34,-34,-32,-35,-31,-31],
Vector(600,100):[-34,-31,-32,-34,-22,]})


#loc_val_dict={}
loc_val_list=[Vector(600,400),Vector(300,200),Vector(1000,400),Vector(1400,400),Vector(200,600),Vector(600,100)]

def calc_range(vect1,vect2):
    xdiff=vect1.x-vect2.x
    ydiff=vect1.y-vect2.y
    return math.sqrt(xdiff**2+ydiff**2)


def distance_RSSI_list(pi):
    for point in loc_val_list: #runs through every sender_location
        distancee=calc_range(point,pi.position) #calculates distance from sender location and pi
        for RSSIi in pi.RSSI_dict[point]:#runs through every RSSI value of the pie at the current sender location
            pi.dist_RSSI.append([distancee,RSSIi])
"""
def distance_RSSI_list(pi): #average
    for point in loc_val_list: #runs through every sender_location
        distancee=calc_range(point,pi.position) #calculates distance from sender location and pi
        pi.dist_RSSI.append([distancee,sum(pi.RSSI_dict[point])/len(pi.RSSI_dict[point])]) #takes average
"""

distance_RSSI_list(pi2)
distance_RSSI_list(pi3)
distance_RSSI_list(pi4)

def calc_distance_reg(rssi):
    return math.exp(-0.1339046599*rssi+ 2.363818961)

def calc_RSSI_distance(distance):
    rssi=-7.468*np.log(0.0940603237047770*distance)
    return(rssi)

lineY=[]
lineX=np.arange(360,1470+1,1)
for point in lineX:
    lineY.append(calc_RSSI_distance(point))

plt.plot(lineX,lineY,marker="o", markersize=1, markeredgecolor="orange", markerfacecolor="orange",label="approximate corrolation")

#def CalculateDistance(rssi, tx_power=39, n=2):
#    return 10 ** ((tx_power - rssi) / (10 * n))

for point in pi2.dist_RSSI:
    plt.plot(point[0],point[1],marker="o", markersize=9, markeredgecolor="red", markerfacecolor="red")
#plt.plot(pi2.dist_RSSI[0],pi2.dist_RSSI[1],marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red", label='pi2')

for point in pi3.dist_RSSI:
    plt.plot(point[0],point[1],marker="o", markersize=7, markeredgecolor="green", markerfacecolor="green")
#plt.plot(pi2.dist_RSSI[0],pi2.dist_RSSI[1],marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red", label='pi3')

for point in pi4.dist_RSSI:
    plt.plot(point[0],point[1],marker="o", markersize=5, markeredgecolor="blue", markerfacecolor="blue")    
#plt.plot(pi2.dist_RSSI[0],pi2.dist_RSSI[1],marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red", label='pi4')


#-7.468 log(0.0940603237047770 distance) #log is natural logerithm
plt.xlabel("Distance [cm]")
plt.ylabel("RSSI")
plt.legend()
plt.grid()
plt.show()


for point in pi2.dist_RSSI:
    print(f"{int(point[0])},{point[1]}")
for point in pi3.dist_RSSI:
    print(f"{int(point[0])},{point[1]}")
for point in pi4.dist_RSSI:
    print(f"{int(point[0])},{point[1]}")
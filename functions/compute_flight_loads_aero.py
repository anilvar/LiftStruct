import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#spanwise and chordwise distribution functions asssigned during design


#loops over the aircraft wings and computes the aerodynamic loads
def compute_flight_loads_aero(aircraft):

    #loop over the main wings
    for i in range(0,len(aircraft.main_wing)):
        
        max_load = 2*design_load/aircraft.main_wing[i].span

        for el in range(0,len(aircraft.main_wing.elemlist_upper)):
            compute_element_load(aircraft.main_wing.elemlist_upper[el],aircraft.pointlist,max_load)



        for el in range(0,len(aircraft.main_wing.elemlist_lower)):
            compute_element_load(aircraft.main_wing.elemlist_lower[el],aircraft.pointlist,max_load)








def compute_element_load(local_element,pointlist,max_load):

    local_element.f = [0.0,0.0,0.0]
    local_load = 0.0

    for i in range(0,4):
        spanwise_load  = compute_spanwise_load(pointlist[local_element[elem_val].g[i]])
        chordwise_load = compute_chordwise_load(pointlist[local_element[elem_val].g[i]])
        
        load_scale = max_load
        pointload  = load_scale*spanwise_load*chordwise_load

        local_load  += 0.25*pointload


    if(local_element.surface == 'upper'):
        for i in range(0,4):
            pointlist[local_element[elem_val].g[i]].load_upper+= 0.25*local_load


    if(local_element.surface == 'lower'):
        for i in range(0,4):
            pointlist[local_element[elem_val].g[i]].load_lower+= 0.25*local_load




def compute_spanwise_load(point):

    #triangular distribution
    spanwise_load = 1-point.global_spanwise_coordinate
    return spanwise_load



def compute_chordwise_load(point):

    #triangular distribution
    chordwise_load = 2.0*(1.0-point.chordwise_coordinate)/point.local_chord

    return chordwise_load


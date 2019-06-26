import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#currently look only at the main wing and the fuselage

#the function marks the lower surface of the fuselage (payload) and the wing lower surface (fuel loads)
#loop over the wings
#check if the contains_fuel tag is active
#pull out the starting and ending  x,y and z of the fule loads
#loop over the wing lower surface
#add the fuel load weight
from pyFSI.functions.get_element_ownership import get_element_ownership


def get_the_element_bounds(aircraft,elemlist,pointlist,bdf_structural_meshfile):

#loop over the wings
    for wing in aircraft.main_wing

        #compute the direction
        dir = np.array(wing.main_wing_section[sec].tip_origin) - np.array(wing.main_wing_section[sec].root_origin)
        wing.main_wing_section[sec].dir = dir /np.linalg.norm(dir)

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
from pyFSI.functions.compute_element_based_aircraft_loads import compute_element_based_aircraft_loads


def compute_intersections(aircraft,elemlist,pointlist,bdf_structural_meshfile):

    #mark the necessary elements
    if(aircraft.loads_marked == 0):
        get_element_ownership(bdf_structural_meshfile,aircraft)
    
    
    #currently only wing fuselage intersection
    
#    #wing
#    wing_surface_numbers = set()
#    
#    wing_surface_numbers.append(aircraft.dv_breakdown.wings[0].lower.new_element_nos)
#    wing_surface_numbers.append(aircraft.dv_breakdown.wings[0].upper.new_element_nos)
#    wing_surface_numbers.append(aircraft.dv_breakdown.wings[0].tip.new_element_nos)
#
#
#    wing_internal_numbers = set()
#
#    wing_internal_numbers.append(aircraft.dv_breakdown.wings[0].spars.new_element_nos)
#    wing_internal_numbers.append(aircraft.dv_breakdown.wings[0].ribs.new_element_nos)
#
#    wing_numbers = set()
#    wing_numbers.append(wing_surface_numbers)
#    wing_numbers.append(wing_internal_numbers)
#        
#
#
#
#
#    #fuselage
#
#    fuselage_surface_numbers = set()
#    fuselage_surface_numbers.append(aircraft.dv_breakdown.fuselages[0].top.new_element_nos)
#    fuselage_surface_numbers.append(aircraft.dv_breakdown.fuselages[0].bottom.new_element_nos)
#    fuselage_surface_numbers.append(aircraft.dv_breakdown.fuselages[0].left.new_element_nos)
#    fuselage_surface_numbers.append(aircraft.dv_breakdown.fuselages[0].right.new_element_nos)
#    fuselage_surface_numbers.append(aircraft.dv_breakdown.fuselages[0].front.new_element_nos)
#    fuselage_surface_numbers.append(aircraft.dv_breakdown.fuselages[0].rear.new_element_nos)
#
#
#
#    fuselage_internal_numbers = set()
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].r1.new_element_nos)
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].r2.new_element_nos)
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].r3.new_element_nos)
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].r4.new_element_nos)
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].l1.new_element_nos)
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].l2.new_element_nos)
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].l3.new_element_nos)
#    fuselage_internal_numbers.append(aircraft.dv_breakdown.fuselages[0].l4.new_element_nos)



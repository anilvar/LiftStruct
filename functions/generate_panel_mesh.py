import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#ensure that element centroid computed

def generate_panel_mesh(elemlist,pointlist,aircraft):


    print "Generating panel mesh"
    #mark the necessary elements
    if(aircraft.loads_marked == 0):
        get_element_ownership(bdf_structural_meshfile,aircraft)
    #loop over the wings
    
    max_distance = 0.0
    aircraft_surface_mesh = []
    
    total_surface_element_count = 0
    
    aircraft_surface_points = []

    for i in range(0,len(aircraft.main_wing)):

        wing_u_surface_element_numbers = []
        wing_l_surface_element_numbers = []

        wing_i_surface_element_numbers_l = set(aircraft.dv_breakdown.wings[i].lower.new_element_nos)
        wing_i_surface_element_numbers_u = set(aircraft.dv_breakdown.wings[i].upper.new_element_nos)
        #aircraft.main_wing[i].total_force = 0.0


        for j in range(0,len(elemlist)):
            if (elemlist[j].pid in wing_i_surface_element_numbers_u):
                wing_u_surface_element_numbers.append(j)
                total_surface_element_count+=1
                for ipoint in range(0,4):
                    aircraft_surface_points.append(elemlist[j].g[ipoint])

            elif((elemlist[j].pid in wing_i_surface_element_numbers_l)):
                wing_l_surface_element_numbers.append(j)
                total_surface_element_count+=1
                for ipoint in range(0,4):
                    aircraft_surface_points.append(elemlist[j].g[ipoint])
        
        aircraft.main_wing[i].upper_surface_elements = wing_u_surface_element_numbers
        aircraft.main_wing[i].lower_surface_elements = wing_l_surface_element_numbers


    if (aircraft.fuselage):
        for i in range(0,len(aircraft.fuselage)):
            fuselage_surface_element_numbers = []
            fuselage_i_surface_element_numbers_left = set(aircraft.dv_breakdown.fuselages[i].left.new_element_nos)
            fuselage_i_surface_element_numbers_right = set(aircraft.dv_breakdown.fuselages[i].right.new_element_nos)
            fuselage_i_surface_element_numbers_top = set(aircraft.dv_breakdown.fuselages[i].top.new_element_nos)
            fuselage_i_surface_element_numbers_bottom = set(aircraft.dv_breakdown.fuselages[i].bottom.new_element_nos)
            fuselage_i_surface_element_numbers_front = set(aircraft.dv_breakdown.fuselages[i].front.new_element_nos)
            fuselage_i_surface_element_numbers_rear = set(aircraft.dv_breakdown.fuselages[i].rear.new_element_nos)
        

            for j in range(0,len(elemlist)):
                 if ((elemlist[j].pid in fuselage_i_surface_element_numbers_left) or (elemlist[j].pid in fuselage_i_surface_element_numbers_right) or (elemlist[j].pid in fuselage_i_surface_element_numbers_top) or  (elemlist[j].pid in fuselage_i_surface_element_numbers_bottom) or (elemlist[j].pid in fuselage_i_surface_element_numbers_front) or (elemlist[j].pid in fuselage_i_surface_element_numbers_rear)):
                 
                 
                    fuselage_surface_element_numbers.append(j)
                    total_surface_element_count+=1
                    for ipoint in range(0,4):
                        aircraft_surface_points.append(elemlist[j].g[ipoint])
                 
            aircraft.fuselage[i].surface_elements = fuselage_surface_element_numbers
                 
    direct_map_points = [ int() for i in range(len(pointlist))]
    direct_map_elements = [ int() for i in range(len(elemlist))]
    aircraft.surface_mesh_points = list(set(aircraft_surface_points))
    aircraft.no_of_surface_elements = total_surface_element_count

    inverse_map_points = [ int() for i in range(len(aircraft.surface_mesh_points))]
    inverse_map_elements = [ int() for i in range(aircraft.no_of_surface_elements)]

    for i in range(0,len(aircraft.surface_mesh_points)):
        direct_map_points[aircraft.surface_mesh_points[i]] = i

    aircraft.direct_map_points = direct_map_points

    write_panel_mesh(aircraft,elemlist,pointlist)


def write_panel_mesh(aircraft,elemlist,pointlist):

    mesh_def = open("sample_panel.pnl","wb")
    mesh_def.write(format(len(aircraft.surface_mesh_points)))
    mesh_def.write("\n")
    mesh_def.write(format(aircraft.no_of_surface_elements))
    mesh_def.write("\n")
    
    for i in range(0,len(aircraft.surface_mesh_points)):
    
        mesh_def.write(format(pointlist[aircraft.surface_mesh_points[i]-1].x[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[aircraft.surface_mesh_points[i]-1].x[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[aircraft.surface_mesh_points[i]-1].x[2]))
        mesh_def.write("\n")


    for i in range(0,len(aircraft.main_wing)):
        for j in range(0,len(aircraft.main_wing[i].upper_surface_elements)):
            for k in range(0,4):
                mesh_def.write(format(aircraft.direct_map_points[elemlist[aircraft.main_wing[i].upper_surface_elements[j]].g[k]]))
                mesh_def.write("\t")
            mesh_def.write("\n")

    if(aircraft.fuselage):
        for i in range(0,len(aircraft.fuselage)):
            for j in range(0,len(aircraft.main_wing[i].upper_surface_elements)):
                for k in range(0,4):
                    mesh_def.write(format(aircraft.direct_map_points[elemlist[aircraft.main_wing[i].upper_surface_elements[j]].g[k]]))
                    mesh_def.write("\t")
                mesh_def.write("\n")


    mesh_def.close()

    print "Done writing the aero panel mesh"


#def compute_wing_wake(wing,elemlist,pointlist):
#                 
#    upper_surface_points = []
#    lower_surface_points = []
#    
#    for i in range(0,len(wing.upper_surface_elements)):
#        if (elemlist[wing.upper_surface_elements[i]].type == "CQUAD4"):
#            element_points = 4
#                 
#        elif (elemlist[wing.upper_surface_elements[i]].type == "CTRIA3"):
#            element_points = 3
#                 
#        for j in range(0,element_points):
#            upper_surface_points.append(elemlist[wing.upper_surface_elements[i]].g[j])
#                 
#                 
#    upper_surface_points_set =set(upper_surface_points)
#
#                 
#
#     
#    for i in range(0,len(wing.lower_surface_elements)):
#        if (elemlist[wing.lower_surface_elements[i]].type == "CQUAD4"):
#            element_points = 4
#    
#        elif (elemlist[wing.lower_surface_elements[i]].type == "CTRIA3"):
#            element_points = 3
#    
#        for j in range(0,element_points):
#            lower_surface_points.append(elemlist[wing.lower_surface_elements[i]].g[j])
#    
#    
#    lower_surface_points_set =set(lower_surface_points)
#                
#    intersection_points = set.intersection(upper_surface_points_set,lower_surface_points_set)
#
#    #remove points belonging to the leading edge

    





                 
                 
                 
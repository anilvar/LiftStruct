import numpy as np
import matplotlib.pyplot as plt
import copy
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
from pyFSI.input.read_bdf_file import read_bdf_file
from pyFSI.input.read_bdf_file import read_nas_file
from pyFSI.utility_functions.compute_centroid import compute_centroid
from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3

from pyFSI.interpolation import extrap_matrix
from pyFSI.interpolation import extrap_a2s
from pyFSI.interpolation import extrap_s2a
from pyFSI.interpolation import write_N
from pyFSI.interpolation import read_N




def setup_aero_pointwise(aircraft,elemlist,pointlist):

    [no_of_materials_1,no_of_points_1,no_of_elements_1,pointlist_1,elemlist_1] = read_nas_file("upper_surface4.nas")

    #[elemlist_1,pointlist_1,no_of_points_1,no_of_elements_1,material_list_1,no_of_materials_1,shell_element_list_1,no_of_shell_elements_1,constrained_grid_point_list_1,no_of_constrained_grid_points_1] = read_bdf_file("upper_surface.nas",1.0)

    compute_centroid(elemlist_1,pointlist_1)
    
    print "no of elem :",len(elemlist_1)
#    [elemlist_2,pointlist_2,no_of_points_2,no_of_elements_2,material_list_2,no_of_materials_2,shell_element_list_2,no_of_shell_elements_2,constrained_grid_point_list_2,no_of_constrained_grid_points_2] = read_bdf_file("lower_surface.nas",1.0)

    [no_of_materials_2,no_of_points_2,no_of_elements_2,pointlist_2,elemlist_2] = read_nas_file("lower_surface4.nas")
    
    compute_centroid(elemlist_2,pointlist_2)
    aircraft.main_wing[0].total_force = 0.0

    for j in range(0,len(elemlist_1)):
    
        #compute the point direction relative to the wing root
        
        local_point = np.array(elemlist_1[j].centroid)

            
        point_dir = (local_point - np.array(aircraft.main_wing[0].root_origin))
            
        local_span = np.linalg.norm(point_dir)
            
        point_dir = point_dir/np.linalg.norm(point_dir)
        
        
        
        point_projection_angle = np.arccos(np.dot(point_dir,aircraft.main_wing[0].spanwise_direction)) #assumes both are unit vectors
        
        elemlist_1[j].global_spanwise_coordinate = local_span*np.cos(point_projection_angle)/aircraft.main_wing[0].summed_span
        
        elemlist_1[j].local_chord = aircraft.main_wing[0].chord_surrogate(elemlist_1[j].global_spanwise_coordinate)
        
        
        #breakup the load
        
        max_load   = 2.0*aircraft.main_wing[0].sizing_lift/aircraft.main_wing[0].span
        load_scale = max_load
        element_load = load_scale*compute_spanwise_load(elemlist_1[j])*compute_chordwise_load(elemlist_1[j])
        elemlist_1[j].pressure = element_load
        element_load = element_load*elemlist_1[j].area
        
        aircraft.main_wing[0].total_force += element_load
        
        if(elemlist_1[j].type == "CTRIA3"):
            for ijk in range(0,3):
                pointlist_1[elemlist_1[j].g[ijk]-1].load+= 0.33*element_load
                if(aircraft.main_wing[0].vertical == 0):
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[0] += 0.0
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[1] += 0.33*element_load
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[2] += 0.0
                else:
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[0] += 0.0
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[1] += 0.0
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[2] += 0.33*element_load




        if(elemlist_1[j].type == "CQUAD4"):
            for ijk in range(0,4):
                pointlist_1[elemlist_1[j].g[ijk]-1].load+= 0.25*element_load
                if(aircraft.main_wing[0].vertical == 0):
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[0] += 0.0
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[1] += 0.25*element_load
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[2] += 0.0
                else:
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[0] += 0.0
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[1] += 0.0
                    pointlist_1[elemlist_1[j].g[ijk]-1].f[2] += 0.25*element_load

                   
                   
                   
    for j in range(0,len(elemlist_2)):
       
       #compute the point direction relative to the wing root
       
       local_point = np.array(elemlist_2[j].centroid)
       
       point_dir = (local_point - np.array(aircraft.main_wing[0].root_origin))
       
       local_span = np.linalg.norm(point_dir)
       
       point_dir = point_dir/np.linalg.norm(point_dir)
       
       
       
       point_projection_angle = np.arccos(np.dot(point_dir,aircraft.main_wing[0].spanwise_direction)) #assumes both are unit vectors
       
       elemlist_2[j].global_spanwise_coordinate = local_span*np.cos(point_projection_angle)/aircraft.main_wing[0].summed_span
       
       elemlist_2[j].local_chord = aircraft.main_wing[0].chord_surrogate(elemlist_2[j].global_spanwise_coordinate)
       
       
       #breakup the load
       
       max_load   = 2.0*aircraft.main_wing[0].sizing_lift/aircraft.main_wing[0].span
       load_scale = max_load
       element_load = load_scale*compute_spanwise_load(elemlist_2[j])*compute_chordwise_load(elemlist_2[j])
       elemlist_2[j].pressure = element_load
       element_load = element_load*elemlist_2[j].area
       
       aircraft.main_wing[0].total_force += element_load
       
       if(elemlist_2[j].type == "CTRIA3"):
           for ijk in range(0,3):
               pointlist_2[elemlist_2[j].g[ijk]-1].load+= 0.33*element_load
               if(aircraft.main_wing[0].vertical == 0):
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[0] += 0.0
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[1] += 0.33*element_load
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[2] += 0.0
               else:
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[0] += 0.0
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[1] += 0.0
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[2] += 0.33*element_load
       
       
       
       
       if(elemlist_2[j].type == "CQUAD4"):
           for ijk in range(0,4):
               pointlist_2[elemlist_2[j].g[ijk]-1].load+= 0.25*element_load
               if(aircraft.main_wing[0].vertical == 0):
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[0] += 0.0
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[1] += 0.25*element_load
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[2] += 0.0
               else:
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[0] += 0.0
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[1] += 0.0
                   pointlist_2[elemlist_2[j].g[ijk]-1].f[2] += 0.25*element_load

                  
                  
                  



#    #Visualize the results -----------------------------------------------------------
#    fig = plt.figure(1)
#    plt.xlabel('x axis')
#    plt.ylabel('y axis')
#    
#    ax = Axes3D(fig)
#    
#    for i in range (0,len(pointlist_1)):
#        if((pointlist_1[i].f[0]>0.000001) or (pointlist_1[i].f[1]>0.000001) or (pointlist_1[i].f[2]>0.000001)):
#            
#            ax.scatter(pointlist_1[i].x[0], pointlist_1[i].x[1], pointlist_1[i].f[1],c="red")
#
#    plt.savefig("3d_loads_plot.png",format='png')
#    
#    plt.show()
#    plt.clf()
#        
#        
#        
#    loads = np.zeros(len(pointlist_1))
#    y_position = np.zeros(len(pointlist_1))
#    for i in range(0,len(pointlist_1)):
#        
#        if((pointlist_1[i].f[0]>0.000001) or (pointlist_1[i].f[1]>0.000001) or (pointlist_1[i].f[2]>0.000001)):
#            loads[i] = pointlist_1[i].f[1]
#            y_position[i] = pointlist_1[i].x[1]
#
#
#    fig2 = plt.figure(2)
#    plt.xlabel('y location')
#    plt.ylabel('loads')
#    plt.plot(y_position,loads,'*')
#    plt.savefig("2D_loads_distribution.png",format='png')
#    plt.clf()
#    #---------------------------------------------------------------------------------------

    #interpolate the loads
    pointlist2 = copy.deepcopy(pointlist)


    print "Interpolating loadset 1:"
    N1,N_list_dx1 = extrap_matrix(pointlist_1, pointlist2, elemlist)
    extrap_a2s(pointlist_1,pointlist2,elemlist,N_list_dx1, N1)
    
    print "Interpolating loadset 2:"
    N2,N_list_dx2 = extrap_matrix(pointlist_2, pointlist, elemlist)
    extrap_a2s(pointlist_2,pointlist,elemlist,N_list_dx2, N2)
                  
    for i in range(0,len(pointlist)):
        pointlist[i].f[0] +=pointlist2[i].f[0]
        pointlist[i].f[1] +=pointlist2[i].f[1]
        pointlist[i].f[2] +=pointlist2[i].f[2]
                  



def compute_spanwise_load(element):
    
    #triangular distribution
    spanwise_load = 1.0-element.global_spanwise_coordinate
    return spanwise_load



def compute_chordwise_load(element):
    
    #uniform
    chordwise_load = 1.0/element.local_chord
    
    
    #triangular distribution
    #chordwise_load = 2.0*(1.0-element.chordwise_coordinate)/element.local_chord
    
    return chordwise_load
                  


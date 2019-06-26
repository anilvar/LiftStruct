import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3

#create a wing spans array - wing_spans
#compute the total wing span  - summed_span
#compute the spanwise chord interpolation
#compute the spanwise direction - aircraft.main_wing[i].main_wing_section[j].spanwise_direction

def aircraft_aero_mesh_generation(aircraft):

#compute

    no_of_spanwise_points = 100
    no_of_chordwise_points = 20

    #loop over the wings

    #loop over the main wings
    for i in range(0,len(aircraft.main_wing)):

        wing_fraction = np.zeros(len(aircraft.main_wing[i].main_wing_section))
        
        #compute the sums of the wing fractions
        for j in range(0,len(aircraft.main_wing[i].main_wing_section)):
            wing_fraction[j] = aircraft.main_wing[i].wing_spans[j]/aircraft.main_wing[i].summed_span

        #compute the no of spanwise elements
        for j in range(0,len(aircraft.main_wing[i].main_wing_section)):
            aircraft.main_wing[i].main_wing_section[j].no_of_spanwise_aero_points = int(wing_fraction[j]*100)
            aircraft.main_wing[i].main_wing_section[j].total_no_of_aero_points    = aircraft.main_wing[i].main_wing_section[j].no_of_spanwise_aero_points*no_of_chordwise_points
            aircraft.main_wing[i].main_wing_section[j].dspan   = aircraft.main_wing[i].wing_spans[j]/float(aircraft.main_wing[i].main_wing_section[j].no_of_spanwise_aero_points)



        #setting up the aero points and elements
        pointlist = [ grid() for i in range(aircraft.main_wing[i].main_wing_section[j].total_no_of_aero_points)]

        aircraft.main_wing[i].main_wing_section[j].no_of_elements   = (no_of_chordwise_points-1)*(aircraft.main_wing[i].main_wing_section[j].no_of_spanwise_aero_points-1)

        elemlist_upper = [ CTRIA3() for i in range(aircraft.main_wing[i].main_wing_section[j].no_of_elements)]
        elemlist_lower = [ CTRIA3() for i in range(aircraft.main_wing[i].main_wing_section[j].no_of_elements)]


        #creating the grid
        
        #set up the points--------------------------------------------------
        pointlist_count  = 0
        for j in range(0,len(aircraft.main_wing[i].main_wing_section)):
            
            root_origin = aircraft.main_wing[i].main_wing_section[j].root_origin
            wing_section_spanwise_direction = aircraft.main_wing[i].main_wing_section[j].spanwise_direction
            d_span = aircraft.main_wing[i].main_wing_section[j].dspan
            
            for sp_pt in range(0,aircraft.main_wing[i].main_wing_section[j].no_of_spanwise_aero_points):
                for ch_pt in range(0,no_of_chordwise_points):
                    
                    pointlist[pointlist_count].spanwise_coordinate = float(sp_pt)*aircraft.main_wing[i].main_wing_section[j].dspan
                    pointlist[pointlist_count].spanwise_index      = sp_pt
                    
                    pointlist[pointlist_count].global_spanwise_coordinate = (aircraft.main_wing[i].wing_spans_cumulative[j] + pointlist[pointlist_count].spanwise_coordinate)/aircraft.main_wing[i].summed_span
                    
                    
                    local_chord = aircraft.main_wing[i].main_wing_section[j].chord_surrogate(pointlist[pointlist_count].spanwise_coordinate)
                    
                    d_chord  = local_chord/float(no_of_chordwise_points)
                    starting_x_index = root_origin[0] - local_chord/2.0
                    ending_x_index   = root_origin[0] + local_chord/2.0
                    
                    pointlist[pointlist_count].local_chord         = local_chord


                    pointlist[pointlist_count].chordwise_index     = ch_pt
                    pointlist[pointlist_count].chordwise_coordinate = (float(ch_pt)*d_chord)/local_chord


                    local_origin = root_origin + wing_section_spanwise_direction*d_span
                    pointlist[pointlist_count].x[0] = starting_x_index + pointlist[pointlist_count].chordwise_coordinate
                    pointlist[pointlist_count].x[1] = local_origin[1]
                    pointlist[pointlist_count].x[2] = local_origin[2]

                    pointlist[pointlist_count].type = 'GRID'
                    pointlist[pointlist_count].id  = pointlist_count + 1
                    pointlist[pointlist_count].cp = 0.0
                    pointlist[pointlist_count].pressure = 0.0
                    pointlist[pointlist_count].normal = [0.0,0.0,0.0]
                    
                    pointlist[pointlist_count].f[0] = 0.0
                    pointlist[pointlist_count].f[1] = 0.0
                    pointlist[pointlist_count].f[2] = 0.0
                    
                    pointlist[pointlist_count].load_upper = 0.0
                    pointlist[pointlist_count].load_lower = 0.0


                    pointlist_count = pointlist_count + 1



            #set up the elements---------------------------------------------
            elem_points_span = 0
            elem_points_chord = 0
            wing_section_no_of_spanwise_points = aircraft.main_wing[i].main_wing_section[j].no_of_spanwise_aero_points
            for elem_val in range(0,aircraft.main_wing[i].main_wing_section[j].no_of_elements):
                elemlist_upper[elem_val].type = 'CQUAD4'
                elemlist_upper[elem_val].eid  = elem_val + 1
                elemlist_upper[elem_val].g[0] = pointlist[elem_points_span*no_of_chordwise_points + elem_points_chord].id
                elemlist_upper[elem_val].g[1] = pointlist[(elem_points_span+1)*no_of_chordwise_points + elem_points_chord].id
                elemlist_upper[elem_val].g[2] = pointlist[(elem_points_span+1)*no_of_chordwise_points + (elem_points_chord+1)].id
                elemlist_upper[elem_val].g[3] = pointlist[elem_points_span*no_of_chordwise_points + (elem_points_chord +1)].id
                
                elemlist_upper[elem_val].surface = 'upper'
                
                #compute the centroid, area of the elements, and normal
                
                elemlist_upper[elem_val].centroid = [0.0,0.0,0.0]
                elemlist_upper[elem_val].normal   = [0.0,0.0,0.0]
                elemlist_upper[elem_val].area     = 0.0
                
                #compute the centroid
                for cent in range(0,4):
                    elemlist_upper[elem_val].centroid[0] += 0.25*pointlist[elemlist_upper[elem_val].g[cent]].x[0]
                    elemlist_upper[elem_val].centroid[1] += 0.25*pointlist[elemlist_upper[elem_val].g[cent]].x[1]
                    elemlist_upper[elem_val].centroid[2] += 0.25*pointlist[elemlist_upper[elem_val].g[cent]].x[2]
                
                #compute the normal (not mandatory currently)
                
                #compute the area
                d_chord1  = pointlist[elemlist_upper[elem_val].g[0]].local_chord/float(no_of_chordwise_points)
                d_chord2  = pointlist[elemlist_upper[elem_val].g[1]].local_chord/float(no_of_chordwise_points)
                temp_area = 0.5*d_span*(d_chord1 + d_chord2 ) #trapezoidal area
                elemlist_upper[elem_val].area = temp_area
                
                
                
                
                
                elemlist_lower[elem_val].type = 'CQUAD4'
                elemlist_lower[elem_val].eid  = elem_val + 1
                elemlist_lower[elem_val].g[0] = pointlist[elem_points_span*no_of_chordwise_points + elem_points_chord].id
                elemlist_lower[elem_val].g[3] = pointlist[(elem_points_span+1)*no_of_chordwise_points + elem_points_chord].id
                elemlist_lower[elem_val].g[2] = pointlist[(elem_points_span+1)*no_of_chordwise_points + (elem_points_chord+1)].id
                elemlist_lower[elem_val].g[1] = pointlist[elem_points_span*no_of_chordwise_points + (elem_points_chord +1)].id

                elemlist_lower[elem_val].centroid = [0.0,0.0,0.0]
                elemlist_lower[elem_val].normal   = [0.0,0.0,0.0]
                elemlist_lower[elem_val].area     = 0.0
                
                elemlist_lower[elem_val].surface = 'lower'
                
                #compute the centroid
                for cent in range(0,4):
                    elemlist_lower[elem_val].centroid[0] += 0.25*pointlist[elemlist_lower[elem_val].g[cent]].x[0]
                    elemlist_lower[elem_val].centroid[1] += 0.25*pointlist[elemlist_lower[elem_val].g[cent]].x[1]
                    elemlist_lower[elem_val].centroid[2] += 0.25*pointlist[elemlist_lower[elem_val].g[cent]].x[2]
                
                #compute the normal (not mandatory currently)
                
                #compute the area
                elemlist_lower[elem_val].area = elemlist_upper[elem_val].area


                




                if(elem_points_chord<=(no_of_chordwise_points-1)):
                    elem_points_chord+=1
                else:
                    elem_points_span+=1
                    elem_points_chord=0


            #pack the aero points and elements
            aircraft.main_wing[i].aero_points = pointlist
            aircraft.main_wing[i].aero_elements = elemlist




            #




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


def compute_flight_loads(aircraft,elemlist,pointlist,bdf_structural_meshfile):

    #mark the necessary elements
    if(aircraft.loads_marked == 0):
        get_element_ownership(bdf_structural_meshfile,aircraft)
    
    
    compute_element_based_aircraft_loads(elemlist,pointlist,aircraft)
    
    #need to loop over the structural mesh and look at the wing lower surface elements
    wing_lower_surface_element_numbers = set(aircraft.dv_breakdown.wings[0].lower.new_element_nos)


    fuse_lower_surface_element_numbers = set([])
    if(aircraft.fuselage):
        fuse_lower_surface_element_numbers = set(aircraft.dv_breakdown.fuselages[0].bottom.new_element_nos)
       
    wing_loading_points = []
    fuse_loading_points = []

    for i in range(0,len(elemlist)):
        if elemlist[i].type == "CQUAD4" :
            for edg in range(0,3):
                elemlist[i].centroid[edg] = (pointlist[elemlist[i].g[0]-1].x[edg] + pointlist[elemlist[i].g[1]-1].x[edg]  + pointlist[elemlist[i].g[2]-1].x[edg]  + pointlist[elemlist[i].g[3]-1].x[edg] )/4.0
        

        elif elemlist[i].type == "CTRIA3" :
            for edg in range(0,3):
                elemlist[i].centroid[edg] = (pointlist[elemlist[i].g[0]-1].x[edg]  + pointlist[elemlist[i].g[1]-1].x[edg]  + pointlist[elemlist[i].g[2]-1].x[edg] )/3.0


    # for the wing loop over the elements (check if the numbers match those in the list and if so store the poin,id in a list


    for i in range(0,len(elemlist)):
        
        if (elemlist[i].pid in wing_lower_surface_element_numbers):
            
            if(elemlist[i].centroid[0] <= aircraft.main_wing[0].max_x) and (elemlist[i].centroid[1] <= aircraft.main_wing[0].max_y) and (elemlist[i].centroid[2] < aircraft.main_wing[0].max_z):
            
                for j in range(0,3):
                    wing_loading_points.append(elemlist[i].g[j])

                if (elemlist[i].type == "CQUAD4") :
                    wing_loading_points.append(elemlist[i].g[3])


        if (elemlist[i].pid in fuse_lower_surface_element_numbers):
            for j in range(0,3):
                fuse_loading_points.append(elemlist[i].g[j])
            
            if (elemlist[i].type == "CQUAD4") :
                fuse_loading_points.append(elemlist[i].g[3])






    #get the pointid for the wing and fuselage loads
    wing_loading_points_listset = list(set(wing_loading_points))


    fuse_loading_points_listset = list(set(fuse_loading_points))


    distributed_fuel_load = aircraft.main_wing[0].fuel_load*9.81 / float(len(wing_loading_points_listset))

    if(aircraft.fuselage):
        distributed_payload = aircraft.payload*9.81 / float(len(fuse_loading_points_listset))

    #now add the point loads at the points
    for i in range(0,len(wing_loading_points_listset)):
        pointlist[wing_loading_points_listset[i]-1].f[1] += -1.0*float(distributed_fuel_load)
        #print "wing : ",i," : ",-1.0*float(distributed_fuel_load)
        pointlist[wing_loading_points_listset[i]-1].fuel_load_p = 1
        pointlist[wing_loading_points_listset[i]-1].fuel_load = -1.0*float(distributed_fuel_load)

    if(aircraft.fuselage):
        for i in range(0,len(fuse_loading_points_listset)):
            pointlist[fuse_loading_points_listset[i]-1].f[1] += -1.0*float(distributed_payload)
            pointlist[fuse_loading_points_listset[i]-1].payload_p = 1
            pointlist[fuse_loading_points_listset[i]-1].payload = -1.0*float(distributed_payload)


    aircraft.no_of_points_w_fuel_load = len(wing_loading_points_listset)
    aircraft.no_of_points_w_payload = len(fuse_loading_points_listset)






    #loop over the elements in the wing lower surface (get the point id's)
    #split the loads uniformly among the lower surface points



#visualization of the loading points
#
#    fig = plt.figure(1)
#        
#    ax = Axes3D(fig)
#        
#        
#    for i in range(0,len(wing_loading_points_listset)):
#        ax.scatter(pointlist[wing_loading_points_listset[i]-1].x[0],pointlist[wing_loading_points_listset[i]-1].x[1],pointlist[wing_loading_points_listset[i]-1].x[2],c="blue")
#
#    
#    for i in range(0,len(fuse_loading_points_listset)):
#        ax.scatter(pointlist[fuse_loading_points_listset[i]-1].x[0],pointlist[fuse_loading_points_listset[i]-1].x[1],pointlist[fuse_loading_points_listset[i]-1].x[2],c="red")
#
#
#
#    plt.savefig('struct_braced_fuel_loads_vis.png',format='png')
#    
#    plt.show()
#    plt.clf()



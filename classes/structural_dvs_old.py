#---Class structure for this----------------------
from pyFSI.class_str.grid.class_structure import grid
from pyFSI.input.read_geomach_surface_points import read_geomach_surface_points
from pyFSI.input.read_stl_meshfile import read_stl_meshfile
from pyFSI.functions.compute_aircraft_loads import compute_aerodynamic_loads
from pyFSI.class_str.material.class_structure import PSHELL
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt

class structural_dvs:
    
    def __init__(self,aircraft_type):
    
    
        if (aircraft_type == 'Conventional'):
            self.fuselage_skin_top = np.zeros(4)
            self.fuselage_skin_bottom = np.zeros(4)
            self.fuselage_skin_left = np.zeros(4)
            self.fuselage_skin_right = np.zeros(4)
            self.fuselage_front = np.zeros(4)
            self.fuselage_rear = np.zeros(4)
            
            self.fuselage_internal_r1 = np.zeros(4)
            self.fuselage_internal_r2 = np.zeros(4)
            self.fuselage_internal_r3 = np.zeros(4)
            self.fuselage_internal_r4 = np.zeros(4)
            
            self.fuselage_internal_l1 = np.zeros(4)
            self.fuselage_internal_l2 = np.zeros(4)
            self.fuselage_internal_l3 = np.zeros(4)
            self.fuselage_internal_l4 = np.zeros(4)
            
            
            self.lwing_upper = np.zeros(4)
            self.lwing_lower = np.zeros(4)
            self.lwing_tip = np.zeros(4)
            self.lwing_spars_s1 = np.zeros(4)
            self.lwing_spars_s2 = np.zeros(4)
            self.lwing_spars_s3 = np.zeros(4)
            self.lwing_ribs = np.zeros(4)
            self.lwing_internal_i1 = np.zeros(4)
            self.lwing_internal_i2 = np.zeros(4)
            
            self.ltail_upper = np.zeros(4)
            self.ltail_lower = np.zeros(4)
            self.ltail_tip = np.zeros(4)
            self.ltail_spars = np.zeros(4)
            self.ltail_ribs = np.zeros(4)
            
            self.vtail_upper = np.zeros(4)
            self.vtail_lower = np.zeros(4)
            self.vtail_tip = np.zeros(4)
            self.vtail_spars = np.zeros(4)
            self.vtail_ribs = np.zeros(4)
            
            self.intersection_lwing_fuse = np.zeros(4)
            self.intersection_ltail_fuse = np.zeros(4)
            self.intersection_vtail_fuse = np.zeros(4)
            
            dv_breakdown_miscellaneous = np.zeros(4)
            self.miscellaneous_w1 = np.zeros(4)
            self.miscellaneous_w2 = np.zeros(4)
            self.miscellaneous_w3 = np.zeros(4)
            self.miscellaneous_w4 = np.zeros(4)
            self.miscellaneous_w5 = np.zeros(4)
            self.miscellaneous_w6 = np.zeros(4)
            self.miscellaneous_t1 = np.zeros(4)
            self.miscellaneous_t2 = np.zeros(4)
            self.miscellaneous_t3 = np.zeros(4)
            self.miscellaneous_f1 = np.zeros(4)
            self.miscellaneous_f2 = np.zeros(4)
            
            self.lstrut_upper = np.zeros(4)
            self.lstrut_lower = np.zeros(4)
            self.lstrut_tip = np.zeros(4)
            self.lstrut_spars = np.zeros(4)
            self.lstrut_ribs = np.zeros(4)
            
            self.lv_upper = np.zeros(4)
            self.lv_lower = np.zeros(4)
            self.lv_tip = np.zeros(4)
            self.lv_spars = np.zeros(4)
            self.lv_ribs = np.zeros(4)
        
            self.total = 0
    

        
        if (aircraft_type == 'Strut_braced'):
            self.fuselage_skin_top = np.zeros(4)
            self.fuselage_skin_bottom = np.zeros(4)
            self.fuselage_skin_left = np.zeros(4)
            self.fuselage_skin_right = np.zeros(4)
            self.fuselage_front = np.zeros(4)
            self.fuselage_rear = np.zeros(4)
            
            self.fuselage_internal_r1 = np.zeros(4)
            self.fuselage_internal_r2 = np.zeros(4)
            self.fuselage_internal_r3 = np.zeros(4)
            self.fuselage_internal_r4 = np.zeros(4)
            
            self.fuselage_internal_l1 = np.zeros(4)
            self.fuselage_internal_l2 = np.zeros(4)
            self.fuselage_internal_l3 = np.zeros(4)
            self.fuselage_internal_l4 = np.zeros(4)
            
            
            self.lwing_upper = np.zeros(4)
            self.lwing_lower = np.zeros(4)
            self.lwing_tip = np.zeros(4)
            self.lwing_spars_s1 = np.zeros(4)
            self.lwing_spars_s2 = np.zeros(4)
            self.lwing_spars_s3 = np.zeros(4)
            self.lwing_ribs = np.zeros(4)
            self.lwing_internal_i1 = np.zeros(4)
            self.lwing_internal_i2 = np.zeros(4)
            
            self.ltail_upper = np.zeros(4)
            self.ltail_lower = np.zeros(4)
            self.ltail_tip = np.zeros(4)
            self.ltail_spars = np.zeros(4)
            self.ltail_ribs = np.zeros(4)
            
            self.vtail_upper = np.zeros(4)
            self.vtail_lower = np.zeros(4)
            self.vtail_tip = np.zeros(4)
            self.vtail_spars = np.zeros(4)
            self.vtail_ribs = np.zeros(4)
            
            self.intersection_lwing_fuse = np.zeros(4)
            self.intersection_ltail_fuse = np.zeros(4)
            self.intersection_vtail_fuse = np.zeros(4)
            
            dv_breakdown_miscellaneous = np.zeros(4)
            self.miscellaneous_w1 = np.zeros(4)
            self.miscellaneous_w2 = np.zeros(4)
            self.miscellaneous_w3 = np.zeros(4)
            self.miscellaneous_w4 = np.zeros(4)
            self.miscellaneous_w5 = np.zeros(4)
            self.miscellaneous_w6 = np.zeros(4)
            self.miscellaneous_t1 = np.zeros(4)
            self.miscellaneous_t2 = np.zeros(4)
            self.miscellaneous_t3 = np.zeros(4)
            self.miscellaneous_f1 = np.zeros(4)
            self.miscellaneous_f2 = np.zeros(4)
            
            self.lstrut_upper = np.zeros(4)
            self.lstrut_lower = np.zeros(4)
            self.lstrut_tip = np.zeros(4)
            self.lstrut_spars = np.zeros(4)
            self.lstrut_ribs = np.zeros(4)
            
            self.lv_upper = np.zeros(4)
            self.lv_lower = np.zeros(4)
            self.lv_tip = np.zeros(4)
            self.lv_spars = np.zeros(4)
            self.lv_ribs = np.zeros(4)
        
            self.total = 0



    def compute_structural_dvs(self,aircraft_type):
        
        
        
        if(aircraft_type=='Conventional'):
        
        
        
            count = 0
            self.fuselage_skin_top[2] = count
            self.fuselage_skin_top[3] = self.fuselage_skin_top[0]
            count += self.fuselage_skin_top[0]

            
            self.fuselage_skin_bottom[2] = count
            self.fuselage_skin_bottom[3] = self.fuselage_skin_bottom[0]
            count += self.fuselage_skin_bottom[0]

            
            self.fuselage_skin_left[2] = count
            self.fuselage_skin_left[3] = self.fuselage_skin_left[0]
            count += self.fuselage_skin_left[0]

            
            self.fuselage_skin_right[2] = count
            self.fuselage_skin_right[3] = self.fuselage_skin_right[0]
            count += self.fuselage_skin_right[0]

            
            self.fuselage_front[2] = count
            self.fuselage_front[3] = self.fuselage_front[0]
            count += self.fuselage_front[0]
            
            
            self.fuselage_rear[2] = count
            self.fuselage_rear[3] = self.fuselage_rear[0]
            count += self.fuselage_rear[0]
            
            self.fuselage_internal_r1[2] = count
            self.fuselage_internal_r1[3] = self.fuselage_internal_r1[0]
            count += self.fuselage_internal_r1[0]
            
            
            self.fuselage_internal_r2[2] = count
            self.fuselage_internal_r2[3] = self.fuselage_internal_r2[0]
            count += self.fuselage_internal_r2[0]
            
            
            self.fuselage_internal_r3[2] = count
            self.fuselage_internal_r3[3] = self.fuselage_internal_r3[0]
            count += self.fuselage_internal_r3[0]
            
            
            self.fuselage_internal_r4[2] = count
            self.fuselage_internal_r4[3] = self.fuselage_internal_r4[0]
            count += self.fuselage_internal_r4[0]
            
            self.fuselage_internal_l1[2] = count
            self.fuselage_internal_l1[3] = self.fuselage_internal_l1[0]
            count += self.fuselage_internal_l1[0]
            
            self.fuselage_internal_l2[2] = count
            self.fuselage_internal_l2[3] = self.fuselage_internal_l2[0]
            count += self.fuselage_internal_l2[0]
            
            
            self.fuselage_internal_l3[2] = count
            self.fuselage_internal_l3[3] = self.fuselage_internal_l3[0]
            count += self.fuselage_internal_l3[0]
            
            
            self.fuselage_internal_l4[2] = count
            self.fuselage_internal_l4[3] = self.fuselage_internal_l4[0]
            count += self.fuselage_internal_l4[0]
            
            
            
            self.lwing_upper[2] = count
            self.lwing_upper[3] = self.lwing_upper[0]
            count += self.lwing_upper[0]
            
            
            self.lwing_lower[2] = count
            self.lwing_lower[3] = self.lwing_lower[0]
            count += self.lwing_lower[0]
            
            
            self.lwing_tip[2] = count
            self.lwing_tip[3] = self.lwing_tip[0]
            count += self.lwing_tip[0]
            
            
            self.lwing_spars_s1[2] = count
            self.lwing_spars_s1[3] = self.lwing_spars_s1[0]
            count += self.lwing_spars_s1[0]
            
            
            self.lwing_spars_s2[2] = count
            self.lwing_spars_s2[3] = self.lwing_spars_s2[0]
            count += self.lwing_spars_s2[0]
            
            
            self.lwing_spars_s3[2] = count
            self.lwing_spars_s3[3] = self.lwing_spars_s3[0]
            count += self.lwing_spars_s3[0]
            
            
            self.lwing_ribs[2] = count
            self.lwing_ribs[3] = self.lwing_ribs[0]
            count += self.lwing_ribs[0]
            
            
            self.lwing_internal_i2[2] = count
            self.lwing_internal_i1[3] = self.lwing_internal_i1[0]
            count += self.lwing_internal_i2[0]
            
            
            self.fuselage_skin_top[2] = count
            self.lwing_internal_i2[3] = self.lwing_internal_i2[0]
            count += self.fuselage_skin_top[0]
            
            self.ltail_upper[2] = count
            self.ltail_upper[3] = self.ltail_upper[0]
            count += self.ltail_upper[0]
            
            
            self.ltail_lower[2] = count
            self.ltail_lower[3] = self.ltail_lower[0]
            count += self.ltail_lower[0]
            
            
            self.ltail_tip[2] = count
            self.ltail_tip[3] = self.ltail_tip[0]
            count += self.ltail_tip[0]
            
            
            self.ltail_spars[2] = count
            self.ltail_spars[3] = self.ltail_spars[0]
            count += self.ltail_spars[0]
            
            
            self.ltail_ribs[2] = count
            self.ltail_ribs[3] = self.ltail_ribs[0]
            count += self.ltail_ribs[0]
            
            self.vtail_upper[2] = count
            self.vtail_upper[3] = self.vtail_upper[0]
            count += self.vtail_upper[0]
            
            
            self.vtail_lower[2] = count
            self.vtail_lower[3] = self.vtail_lower[0]
            count += self.vtail_lower[0]
            
            
            self.vtail_tip[2] = count
            self.vtail_tip[3] = self.vtail_tip[0]
            count += self.vtail_tip[0]
            
            
            self.vtail_spars[2] = count
            self.vtail_spars[3] = self.vtail_spars[0]
            count += self.vtail_spars[0]
            
            
            
            self.vtail_ribs[2] = count
            self.vtail_ribs[3] = self.vtail_ribs[0]
            count += self.vtail_ribs[0]
            
            
            self.intersection_lwing_fuse[2] = count
            self.intersection_lwing_fuse[3] = self.intersection_lwing_fuse[0]
            count += self.intersection_lwing_fuse[0]
            
            
            self.intersection_ltail_fuse[2] = count
            self.intersection_ltail_fuse[3] = self.intersection_ltail_fuse[0]
            count += self.intersection_ltail_fuse[0]
            
            self.intersection_vtail_fuse[2] = count
            self.intersection_vtail_fuse[3] = self.intersection_vtail_fuse[0]
            count += self.intersection_vtail_fuse[0]
            
            
            self.miscellaneous_w1[2] = count
            self.miscellaneous_w1[3] = self.miscellaneous_w1[0]
            count += self.miscellaneous_w1[0]
            
            
            self.miscellaneous_w2[2] = count
            self.miscellaneous_w2[3] = self.miscellaneous_w2[0]
            count += self.miscellaneous_w2[0]
            
            
            self.miscellaneous_w3[2] = count
            self.miscellaneous_w3[3] = self.miscellaneous_w3[0]
            count += self.miscellaneous_w3[0]
            
            
            self.miscellaneous_w4[2] = count
            self.miscellaneous_w4[3] = self.miscellaneous_w4[0]
            count += self.miscellaneous_w4[0]
            
            
            self.miscellaneous_w5[2] = count
            self.miscellaneous_w5[3] = self.miscellaneous_w5[0]
            count += self.miscellaneous_w5[0]
            
            
            self.miscellaneous_w6[2] = count
            self.miscellaneous_w6[3] = self.miscellaneous_w6[0]
            count += self.miscellaneous_w6[0]
            
            
            self.miscellaneous_t1[2] = count
            self.miscellaneous_t1[3] = self.miscellaneous_t1[0]
            count += self.miscellaneous_t1[0]
            
            
            self.miscellaneous_t2[2] = count
            self.miscellaneous_t2[3] = self.miscellaneous_t2[0]
            count += self.miscellaneous_t2[0]
            
            
            self.miscellaneous_t3[2] = count
            self.miscellaneous_t3[3] = self.miscellaneous_t3[0]
            count += self.miscellaneous_t3[0]
            
            
            self.miscellaneous_f1[2] = count
            self.miscellaneous_f1[3] = self.miscellaneous_f1[0]
            count += self.miscellaneous_f1[0]
            
            
            self.miscellaneous_f2[2] = count
            self.miscellaneous_f2[3] = self.miscellaneous_f2[0]
            count += self.miscellaneous_f2[0]
            
            
            
            #for strut braced
            
            self.lstrut_upper[2] = count
            self.lstrut_upper[3] = self.lstrut_upper[0]
            count += self.lstrut_upper[0]
            
            
            self.lstrut_lower[2] = count
            self.lstrut_lower[3] = self.lstrut_lower[0]
            count += self.lstrut_lower[0]
            
            
            self.lstrut_tip[2] = count
            self.lstrut_tip[3] = self.lstrut_tip[0]
            count += self.lstrut_tip[0]
            
            
            self.lstrut_spars[2] = count
            self.lstrut_spars[3] = self.lstrut_spars[0]
            count += self.lstrut_spars[0]
            
            
            self.lstrut_ribs[2] = count
            self.lstrut_ribs[3] = self.lstrut_ribs[0]
            count += self.lstrut_ribs[0]
            
            self.lv_upper[2] = count
            self.lv_upper[3] = self.lv_upper[0]
            count += self.lv_upper[0]
            
            
            self.lv_lower[2] = count
            self.lv_lower[3] = self.lv_lower[0]
            count += self.lv_lower[0]
            
            
            self.lv_tip[2] = count
            self.lv_tip[3] = self.lv_tip[0]
            count += self.lv_tip[0]
            
            
            self.lv_spars[2] = count
            self.lv_spars[3] = self.lv_spars[0]
            count += self.lv_spars[0]
            
            
            
            self.lv_ribs[2] = count
            self.lv_ribs[3] = self.lv_ribs[0]
            count += self.lv_ribs[0]
            #end for strut braced wings
            
            
            
            self.total = count

            self.new_element_map = np.zeros(int(count))

            shell_element_list_new = [ PSHELL() for i in range(int(count))]
            self.shell_element_list_new = shell_element_list_new

            for i in range(0,int(count)):
                self.new_element_map[i] = i+1
                self.shell_element_list_new[i].pid = i+1
                self.shell_element_list_new[i].name = "f"+str(i)







        if(aircraft_type=='Strut_braced'):


            count = 0
            self.fuselage_skin_top[2] = count
            self.fuselage_skin_top[3] = self.fuselage_skin_top[0]
            count += self.fuselage_skin_top[0]
            
            
            self.fuselage_skin_bottom[2] = count
            self.fuselage_skin_bottom[3] = self.fuselage_skin_bottom[0]
            count += self.fuselage_skin_bottom[0]
            
            
            self.fuselage_skin_left[2] = count
            self.fuselage_skin_left[3] = self.fuselage_skin_left[0]
            count += self.fuselage_skin_left[0]
            
            
            self.fuselage_skin_right[2] = count
            self.fuselage_skin_right[3] = self.fuselage_skin_right[0]
            count += self.fuselage_skin_right[0]
            
            
            self.fuselage_front[2] = count
            self.fuselage_front[3] = self.fuselage_front[0]
            count += self.fuselage_front[0]
            
            
            self.fuselage_rear[2] = count
            self.fuselage_rear[3] = self.fuselage_rear[0]
            count += self.fuselage_rear[0]
            
            self.fuselage_internal_r1[2] = count
            self.fuselage_internal_r1[3] = self.fuselage_internal_r1[0]
            count += self.fuselage_internal_r1[0]
            
            
            self.fuselage_internal_r2[2] = count
            self.fuselage_internal_r2[3] = self.fuselage_internal_r2[0]
            count += self.fuselage_internal_r2[0]
            
            
            self.fuselage_internal_r3[2] = count
            self.fuselage_internal_r3[3] = self.fuselage_internal_r3[0]
            count += self.fuselage_internal_r3[0]
            
            
            self.fuselage_internal_r4[2] = count
            self.fuselage_internal_r4[3] = self.fuselage_internal_r4[0]
            count += self.fuselage_internal_r4[0]
            
            self.fuselage_internal_l1[2] = count
            self.fuselage_internal_l1[3] = self.fuselage_internal_l1[0]
            count += self.fuselage_internal_l1[0]
            
            self.fuselage_internal_l2[2] = count
            self.fuselage_internal_l2[3] = self.fuselage_internal_l2[0]
            count += self.fuselage_internal_l2[0]
            
            
            self.fuselage_internal_l3[2] = count
            self.fuselage_internal_l3[3] = self.fuselage_internal_l3[0]
            count += self.fuselage_internal_l3[0]
            
            
            self.fuselage_internal_l4[2] = count
            self.fuselage_internal_l4[3] = self.fuselage_internal_l4[0]
            count += self.fuselage_internal_l4[0]
            
            
            
            self.lwing_upper[2] = count
            self.lwing_upper[3] = self.lwing_upper[0]
            count += self.lwing_upper[0]
            
            
            self.lwing_lower[2] = count
            self.lwing_lower[3] = self.lwing_lower[0]
            count += self.lwing_lower[0]
            
            
            self.lwing_tip[2] = count
            self.lwing_tip[3] = self.lwing_tip[0]
            count += self.lwing_tip[0]
            
            
            self.lwing_spars_s1[2] = count
            self.lwing_spars_s1[3] = self.lwing_spars_s1[0]
            count += self.lwing_spars_s1[0]
            
            
            self.lwing_spars_s2[2] = count
            self.lwing_spars_s2[3] = self.lwing_spars_s2[0]
            count += self.lwing_spars_s2[0]
            
            
            self.lwing_spars_s3[2] = count
            self.lwing_spars_s3[3] = self.lwing_spars_s3[0]
            count += self.lwing_spars_s3[0]
            
            
            self.lwing_ribs[2] = count
            self.lwing_ribs[3] = self.lwing_ribs[0]
            count += self.lwing_ribs[0]
            
            
            self.lwing_internal_i2[2] = count
            self.lwing_internal_i1[3] = self.lwing_internal_i1[0]
            count += self.lwing_internal_i2[0]
            
            
            self.fuselage_skin_top[2] = count
            self.lwing_internal_i2[3] = self.lwing_internal_i2[0]
            count += self.fuselage_skin_top[0]
            
            self.ltail_upper[2] = count
            self.ltail_upper[3] = self.ltail_upper[0]
            count += self.ltail_upper[0]
            
            
            self.ltail_lower[2] = count
            self.ltail_lower[3] = self.ltail_lower[0]
            count += self.ltail_lower[0]
            
            
            self.ltail_tip[2] = count
            self.ltail_tip[3] = self.ltail_tip[0]
            count += self.ltail_tip[0]
            
            
            self.ltail_spars[2] = count
            self.ltail_spars[3] = self.ltail_spars[0]
            count += self.ltail_spars[0]
            
            
            self.ltail_ribs[2] = count
            self.ltail_ribs[3] = self.ltail_ribs[0]
            count += self.ltail_ribs[0]
            
            self.vtail_upper[2] = count
            self.vtail_upper[3] = self.vtail_upper[0]
            count += self.vtail_upper[0]
            
            
            self.vtail_lower[2] = count
            self.vtail_lower[3] = self.vtail_lower[0]
            count += self.vtail_lower[0]
            
            
            self.vtail_tip[2] = count
            self.vtail_tip[3] = self.vtail_tip[0]
            count += self.vtail_tip[0]
            
            
            self.vtail_spars[2] = count
            self.vtail_spars[3] = self.vtail_spars[0]
            count += self.vtail_spars[0]
            
            
            
            self.vtail_ribs[2] = count
            self.vtail_ribs[3] = self.vtail_ribs[0]
            count += self.vtail_ribs[0]
            
            
            self.intersection_lwing_fuse[2] = count
            self.intersection_lwing_fuse[3] = self.intersection_lwing_fuse[0]
            count += self.intersection_lwing_fuse[0]
            
            
            self.intersection_ltail_fuse[2] = count
            self.intersection_ltail_fuse[3] = self.intersection_ltail_fuse[0]
            count += self.intersection_ltail_fuse[0]
            
            self.intersection_vtail_fuse[2] = count
            self.intersection_vtail_fuse[3] = self.intersection_vtail_fuse[0]
            count += self.intersection_vtail_fuse[0]
            
            
            self.miscellaneous_w1[2] = count
            self.miscellaneous_w1[3] = self.miscellaneous_w1[0]
            count += self.miscellaneous_w1[0]
            
            
            self.miscellaneous_w2[2] = count
            self.miscellaneous_w2[3] = self.miscellaneous_w2[0]
            count += self.miscellaneous_w2[0]
            
            
            self.miscellaneous_w3[2] = count
            self.miscellaneous_w3[3] = self.miscellaneous_w3[0]
            count += self.miscellaneous_w3[0]
            
            
            self.miscellaneous_w4[2] = count
            self.miscellaneous_w4[3] = self.miscellaneous_w4[0]
            count += self.miscellaneous_w4[0]
            
            
            self.miscellaneous_w5[2] = count
            self.miscellaneous_w5[3] = self.miscellaneous_w5[0]
            count += self.miscellaneous_w5[0]
            
            
            self.miscellaneous_w6[2] = count
            self.miscellaneous_w6[3] = self.miscellaneous_w6[0]
            count += self.miscellaneous_w6[0]
            
            
            self.miscellaneous_t1[2] = count
            self.miscellaneous_t1[3] = self.miscellaneous_t1[0]
            count += self.miscellaneous_t1[0]
            
            
            self.miscellaneous_t2[2] = count
            self.miscellaneous_t2[3] = self.miscellaneous_t2[0]
            count += self.miscellaneous_t2[0]
            
            
            self.miscellaneous_t3[2] = count
            self.miscellaneous_t3[3] = self.miscellaneous_t3[0]
            count += self.miscellaneous_t3[0]
            
            
            self.miscellaneous_f1[2] = count
            self.miscellaneous_f1[3] = self.miscellaneous_f1[0]
            count += self.miscellaneous_f1[0]
            
            
            self.miscellaneous_f2[2] = count
            self.miscellaneous_f2[3] = self.miscellaneous_f2[0]
            count += self.miscellaneous_f2[0]
            
            
            
            #for strut braced
            
            self.lstrut_upper[2] = count
            self.lstrut_upper[3] = self.lstrut_upper[0]
            count += self.lstrut_upper[0]
            
            
            self.lstrut_lower[2] = count
            self.lstrut_lower[3] = self.lstrut_lower[0]
            count += self.lstrut_lower[0]
            
            
            self.lstrut_tip[2] = count
            self.lstrut_tip[3] = self.lstrut_tip[0]
            count += self.lstrut_tip[0]
            
            
            self.lstrut_spars[2] = count
            self.lstrut_spars[3] = self.lstrut_spars[0]
            count += self.lstrut_spars[0]
            
            
            self.lstrut_ribs[2] = count
            self.lstrut_ribs[3] = self.lstrut_ribs[0]
            count += self.lstrut_ribs[0]
            
            self.lv_upper[2] = count
            self.lv_upper[3] = self.lv_upper[0]
            count += self.lv_upper[0]
            
            
            self.lv_lower[2] = count
            self.lv_lower[3] = self.lv_lower[0]
            count += self.lv_lower[0]
            
            
            self.lv_tip[2] = count
            self.lv_tip[3] = self.lv_tip[0]
            count += self.lv_tip[0]
            
            
            self.lv_spars[2] = count
            self.lv_spars[3] = self.lv_spars[0]
            count += self.lv_spars[0]
            
            
            
            self.lv_ribs[2] = count
            self.lv_ribs[3] = self.lv_ribs[0]
            count += self.lv_ribs[0]
            #end for strut braced wings
            
            
            
            self.total = count
            
            self.new_element_map = np.zeros(int(count))
            
            shell_element_list_new = [ PSHELL() for i in range(int(count))]
            self.shell_element_list_new = shell_element_list_new
            
            for i in range(0,int(count)):
                self.new_element_map[i] = i+1
                self.shell_element_list_new[i].pid = i+1
                self.shell_element_list_new[i].name = "f"+str(i)



class wing_structure:

    def __init__(self,structure_breakdown):



class fuselage_structure:
    
    def __init__(self,structure_breakdown):
        self.fuselage_skin_top = np.zeros(4)
        self.fuselage_skin_bottom = np.zeros(4)
        self.fuselage_skin_left = np.zeros(4)
        self.fuselage_skin_right = np.zeros(4)
        self.fuselage_front = np.zeros(4)
        self.fuselage_rear = np.zeros(4)
        
        self.fuselage_internal_r1 = np.zeros(4)
        self.fuselage_internal_r2 = np.zeros(4)
        self.fuselage_internal_r3 = np.zeros(4)
        self.fuselage_internal_r4 = np.zeros(4)
        
        self.fuselage_internal_l1 = np.zeros(4)
        self.fuselage_internal_l2 = np.zeros(4)
        self.fuselage_internal_l3 = np.zeros(4)
        self.fuselage_internal_l4 = np.zeros(4)



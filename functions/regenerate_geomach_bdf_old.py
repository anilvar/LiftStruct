import numpy as np

from pyFSI.geomach_aircraft_models.conventional5 import Conventional5


#--imports---
import re
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import math


from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3
from pyFSI.class_str.material.class_structure import PSHELL
from pyFSI.class_str.material.class_structure import PBARL
from pyFSI.class_str.material.class_structure import MAT1
from pyFSI.class_str.load_disp_bc.class_structure import FORCE
from pyFSI.class_str.load_disp_bc.class_structure import PLOAD
from pyFSI.class_str.load_disp_bc.class_structure import SPC
from pyFSI.class_str.io.class_structure import SU2_import

from pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from pyFSI.class_str.io.nastran_datatype_write_formats import str_form

from pyFSI.class_str.io.nastran_datatype_write_formats import float_forms
from pyFSI.class_str.io.nastran_datatype_write_formats import int_forms
from pyFSI.utility_functions.pressure_interpolation import pressure_interpolation


from pyFSI.class_str.optimization.constraints.class_structure import DCONSTR
from pyFSI.class_str.optimization.constraints.class_structure import DCONADD
from pyFSI.class_str.optimization.constraints.class_structure import DRESP
from pyFSI.class_str.optimization.constraints.class_structure import DRESP1
from pyFSI.class_str.optimization.constraints.class_structure import DRESP2
from pyFSI.class_str.optimization.constraints.class_structure import DDVAL
from pyFSI.class_str.optimization.constraints.class_structure import DEQUATN
from pyFSI.class_str.optimization.constraints.class_structure import DESVAR
from pyFSI.class_str.optimization.constraints.class_structure import DVPREL1
from pyFSI.class_str.optimization.constraints.class_structure import DVCREL1
from pyFSI.class_str.optimization.constraints.class_structure import DVGRID
from pyFSI.class_str.optimization.constraints.class_structure import DLINK
from pyFSI.class_str.optimization.constraints.class_structure import DOPTPRM

from pyFSI.utility_functions.print_equation import print_equation


from pyFSI.input.read_nas_file import read_nas_file
from pyFSI.utility_functions.interpolate_grid import interpolate_grid
from pyFSI.output.write_tecplot_file import write_tecplot_file
from pyFSI.output.write_tecplot_file_str import write_tecplot_file_str
from pyFSI.input.read_beam_numbers import read_beam_numbers
from pyFSI.input.read_constraints import read_constraints
from pyFSI.input.read_su2_surface_file import read_su2_surface_file

from pyFSI.input.read_beam import read_beam
from pyFSI.input.read_beam_numbers import read_beam_numbers
from pyFSI.input.read_opt_f06_file import read_opt_f06_file
from pyFSI.input.read_opt_f06_file_stress import read_opt_f06_file_stress
from pyFSI.utility_functions.interpolate_grid_brown import interpolate_grid_brown

from pyFSI.input.read_geomach_structural_file import read_geomach_structural_file

from pyFSI.class_str.solution_classes.sol200 import sol200
#from python_nastran_io.class_str.solution_classes.sol101 import sol101
#-----------
#---function to convert integers to required nastran format
from interpolate_loads import interpolate_loads
from pyFSI.output.write_tacs_load_file import write_tacs_load_file
from pyFSI.input.read_bdf_file import read_bdf_file


#read the file

#mark the existing components

#combine them, write the map

#write out the bdf file

#end with a max case where each element is a design variable

#for external components group by j

def regenerate_geomach_bdf(bdf_structural_meshfile,aircraft):
    scaling_factor = 1.0
    elemlist,pointlist,no_of_points,no_of_elements,material_list,no_of_materials,shell_element_list,no_of_shell_elements,constrained_grid_point_list,no_of_constrained_grid_points = read_bdf_file(bdf_structural_meshfile,scaling_factor)

    element_map = np.zeros(no_of_shell_elements)
    dv_breakdown = aircraft.dv_breakdown
    
    
    if(aircraft.type == 'Conventional'):
    
        #count fuse i
        #0 - local count , 1 - i, 2 - j , 3 - placeholder
        #fuselage
        count_fuse = np.zeros(6) #0
        count_fuse_top = np.zeros(6) #0
        count_fuse_lft = np.zeros(6) #0
        count_fuse_rght = np.zeros(6) #0
        count_fuse_bot = np.zeros(6) #0
        
        count_fuse_r = np.zeros(6) #0
        count_fuse_f = np.zeros(6) #0
        count_fus_i_r1 = np.zeros(6) #0
        count_fus_i_r2 = np.zeros(6) #0
        count_fus_i_r3 = np.zeros(6) #0
        count_fus_i_r4 = np.zeros(6) #0
        count_fus_i_l1 = np.zeros(6) #0
        count_fus_i_l2 = np.zeros(6) #0
        count_fus_i_l3 = np.zeros(6) #0
        count_fus_i_l4 = np.zeros(6) #0
        
        #wings
        count_lwing = np.zeros(6) #0
        count_lwing_upp = np.zeros(6) #0
        count_lwing_low = np.zeros(6) #0
        
        count_lwing_t = np.zeros(6) #0
        count_lwing_i_r = np.zeros(6) #0
        count_lwing_i_s = np.zeros(6) #0
        count_lwing_i_sa = np.zeros(6) #0
        count_lwing_i_sb = np.zeros(6) #0
        count_lwing_i_i1 = np.zeros(6) #0
        count_lwing_i_i2 = np.zeros(6) #0
        
        #ltail
        count_ltail = np.zeros(6) #0
        count_ltail_upp = np.zeros(6) #0
        count_ltail_low = np.zeros(6) #0
        
        count_ltail_t = np.zeros(6) #0
        count_ltail_i_r = np.zeros(6) #0
        count_ltail_i_s = np.zeros(6) #0
        
        #vtail
        count_vtail = np.zeros(6) #0
        count_vtail_upp = np.zeros(6) #0
        count_vtail_low = np.zeros(6) #0
        
        
        count_vtail_t = np.zeros(6) #0
        count_vtail_i_r = np.zeros(6) #0
        count_vtail_i_s = np.zeros(6) #0
        
        #intersections
        count_lwing_fuse = np.zeros(6) #0
        count_ltail_fuse = np.zeros(6) #0
        count_vtail_fuse = np.zeros(6) #0
        
        #intersections internal
        count_lwing_Misc_1 = np.zeros(6) #0
        count_lwing_Misc_2 = np.zeros(6) #0
        count_lwing_Misc_3 = np.zeros(6) #0
        count_lwing_Misc_4 = np.zeros(6) #0
        count_lwing_Misc_5 = np.zeros(6) #0
        count_lwing_Misc_6 = np.zeros(6) #0
        count_ltail_Misc_1 = np.zeros(6) #0
        count_ltail_Misc_2 = np.zeros(6) #0
        count_ltail_Misc_3 = np.zeros(6) #0
        count_fus_Misc_1 = np.zeros(6) #0
        count_fus_Misc_2 = np.zeros(6) #0
        
        
        #for strut braced
        
        #ltail
        count_lstrut = np.zeros(6) #0
        count_lstrut_upp = np.zeros(6) #0
        count_lstrut_low = np.zeros(6) #0
        
        count_lstrut_t = np.zeros(6) #0
        count_lstrut_i_r = np.zeros(6) #0
        count_lstrut_i_s = np.zeros(6) #0
        
        #vtail
        count_lv = np.zeros(6) #0
        count_lv_upp = np.zeros(6) #0
        count_lv_low = np.zeros(6) #0
        
        
        count_lv_t = np.zeros(6) #0
        count_lv_i_r = np.zeros(6) #0
        count_lv_i_s = np.zeros(6) #0
        
        #intersections
    #    lstrut_fuse
    #    lstrut_lwing
    #    lv_lwing
    #    lv_lstrut
    #    ltail_vtail

        #------------------------------------------------------------------------------------



        #dv_breakdown.max   #if 0 then use existing breakdown, if 1, then use specified breakdown if -1, then use max breakdown i.e. all elements are desiogn variables

        #each a 2d array
        
        for i in range(0,4):
        
            count_fuse_top[i+1] = dv_breakdown.fuselage_skin_top[i]
            count_fuse_bot[i+1] = dv_breakdown.fuselage_skin_bottom[i]
            count_fuse_lft[i+1] = dv_breakdown.fuselage_skin_left[i]
            count_fuse_rght[i+1] = dv_breakdown.fuselage_skin_right[i]
            count_fuse_f[i+1] = dv_breakdown.fuselage_front[i]
            count_fuse_r[i+1] = dv_breakdown.fuselage_rear[i]
            
            count_fus_i_r1[i+1] = dv_breakdown.fuselage_internal_r1[i]
            count_fus_i_r2[i+1] = dv_breakdown.fuselage_internal_r2[i]
            count_fus_i_r3[i+1] = dv_breakdown.fuselage_internal_r3[i]
            count_fus_i_r4[i+1] = dv_breakdown.fuselage_internal_r4[i]
            
            count_fus_i_l1[i+1] = dv_breakdown.fuselage_internal_l1[i]
            count_fus_i_l2[i+1] = dv_breakdown.fuselage_internal_l2[i]
            count_fus_i_l3[i+1] = dv_breakdown.fuselage_internal_l3[i]
            count_fus_i_l4[i+1] = dv_breakdown.fuselage_internal_l4[i]
            
            
            count_lwing_upp[i+1] = dv_breakdown.lwing_upper[i]
            count_lwing_low[i+1] = dv_breakdown.lwing_lower[i]
            count_lwing_t[i+1] = dv_breakdown.lwing_tip[i]
            count_lwing_i_s[i+1] = dv_breakdown.lwing_spars_s1[i]
            count_lwing_i_sa[i+1] = dv_breakdown.lwing_spars_s2[i]
            count_lwing_i_sb[i+1] = dv_breakdown.lwing_spars_s3[i]
            count_lwing_i_r[i+1] = dv_breakdown.lwing_ribs[i]
            count_lwing_i_i1[i+1] = dv_breakdown.lwing_internal_i1[i]
            count_lwing_i_i2[i+1] = dv_breakdown.lwing_internal_i2[i]
            
            count_ltail_upp[i+1] = dv_breakdown.ltail_upper[i]
            count_ltail_low[i+1] = dv_breakdown.ltail_lower[i]
            count_ltail_t[i+1] = dv_breakdown.ltail_tip[i]
            count_ltail_i_s[i+1] = dv_breakdown.ltail_spars[i]
            count_ltail_i_r[i+1] = dv_breakdown.ltail_ribs[i]
            
            count_vtail_upp[i+1] = dv_breakdown.vtail_upper[i]
            count_vtail_low[i+1] = dv_breakdown.vtail_lower[i]
            count_vtail_t[i+1] = dv_breakdown.vtail_tip[i]
            count_vtail_i_s[i+1] = dv_breakdown.vtail_spars[i]
            count_vtail_i_r[i+1] = dv_breakdown.vtail_ribs[i]
            
            
            
            count_lwing_fuse[i+1] = dv_breakdown.intersection_lwing_fuse[i]
            count_ltail_fuse[i+1] = dv_breakdown.intersection_ltail_fuse[i]
            count_vtail_fuse[i+1] = dv_breakdown.intersection_vtail_fuse[i]
            

            count_lwing_Misc_1[i+1] = dv_breakdown.miscellaneous_w1[i]
            count_lwing_Misc_2[i+1] = dv_breakdown.miscellaneous_w2[i]
            count_lwing_Misc_3[i+1] = dv_breakdown.miscellaneous_w3[i]
            count_lwing_Misc_4[i+1] = dv_breakdown.miscellaneous_w4[i]
            count_lwing_Misc_5[i+1] = dv_breakdown.miscellaneous_w5[i]
            count_lwing_Misc_6[i+1] = dv_breakdown.miscellaneous_w6[i]
            count_ltail_Misc_1[i+1] = dv_breakdown.miscellaneous_t1[i]
            count_ltail_Misc_2[i+1] = dv_breakdown.miscellaneous_t2[i]
            count_ltail_Misc_3[i+1] = dv_breakdown.miscellaneous_t3[i]
            count_fus_Misc_1[i+1] = dv_breakdown.miscellaneous_f1[i]
            count_fus_Misc_2[i+1] = dv_breakdown.miscellaneous_f2[i]
        
        
        #for strut braced
        
            count_lstrut_low[i+1] = dv_breakdown.ltail_lower[i]
            count_lstrut_t[i+1] = dv_breakdown.ltail_tip[i]
            count_lstrut_i_s[i+1] = dv_breakdown.ltail_spars[i]
            count_lstrut_i_r[i+1] = dv_breakdown.ltail_ribs[i]
            
            count_lv_upp[i+1] = dv_breakdown.vtail_upper[i]
            count_lv_low[i+1] = dv_breakdown.vtail_lower[i]
            count_lv_t[i+1] = dv_breakdown.vtail_tip[i]
            count_lv_i_s[i+1] = dv_breakdown.vtail_spars[i]
            count_lv_i_r[i+1] = dv_breakdown.vtail_ribs[i]
        

        #class in aircraft that has the number of dvs
        no_of_dvs = dv_breakdown.total
        #dv_new = np.zeros(no_of_dvs)
        new_element_map = dv_breakdown.new_element_map
        shell_element_list_new = dv_breakdown.shell_element_list_new
        no_of_shell_elements_new = len(shell_element_list_new)
        
        

    #store the shell elements in a map
        #based on the tags combine the elements

        for i in range(0,len(shell_element_list)):
            name = shell_element_list[i].name
            name_s = name.split(':')


    #fuselage

            if(name_s[0] == 'fuse'):
                if(name_s[1] =='top'):
                    count_fuse_top[0] +=1
                
                elif(name_s[1] =='lft'):
                    count_fuse_lft[0] +=1
                
                elif(name_s[1] =='rght'):
                    count_fuse_rght[0] +=1
                
                elif(name_s[1] =='bot'):
                    count_fuse_bot[0] +=1
                
            
            if(name_s[0] == 'fuse_r'):
                count_fuse_r[0] +=1
                
            
            if(name_s[0] == 'fuse_f'):
                count_fuse_f[0] +=1
                
            
            
        #internal components
        
            if(name_s[0] == 'fus_i_r1'):
                count_fus_i_r1[0] +=1
                
            
            if(name_s[0] == 'fus_i_r2'):
                count_fus_i_r2[0] +=1
                
            
            if(name_s[0] == 'fus_i_r3'):
                count_fus_i_r3[0] +=1
                

            if(name_s[0] == 'fus_i_r4'):
                count_fus_i_r4[0] +=1
                


            if(name_s[0] == 'fus_i_l1'):
                count_fus_i_l1[0] +=1
                
            
            if(name_s[0] == 'fus_i_l2'):
                count_fus_i_l2[0] +=1
                
            
            if(name_s[0] == 'fus_i_l3'):
                count_fus_i_l3[0] +=1
                

            if(name_s[0] == 'fus_i_l4'):
                count_fus_i_l4[0] +=1
                
            
            
    #main wing
            
            if(name_s[0] == 'lwing'):
                if(name_s[1] == 'upp'):
                    count_lwing_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_lwing_low[0] +=1

                
            
            if(name_s[0] == 'lwing_t'):
                count_lwing_t[0] +=1
                


        #internal components

            if(name_s[0] == 'lwing_i_r'):
                count_lwing_i_r[0] +=1
                

            if(name_s[0] == 'lwing_i_s'):
                count_lwing_i_s[0] +=1
                
            
            if(name_s[0] == 'lwing_i_sa'):
                count_lwing_i_sa[0] +=1
                
            
            if(name_s[0] == 'lwing_i_sb'):
                count_lwing_i_sb[0] +=1
                
            
            if(name_s[0] == 'lwing_i_i1'):
                count_lwing_i_i1[0] +=1
                

            if(name_s[0] == 'lwing_i_i2'):
                count_lwing_i_i2[0] +=1
                

    #horizontal tail

            if(name_s[0] == 'ltail'):
                if(name_s[1] == 'upp'):
                    count_ltail_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_ltail_low[0] +=1

                
            

            if(name_s[0] == 'ltail_t'):
                count_ltail_t[0] +=1
                


        #internal components

            if(name_s[0] == 'ltail_i_r'):
                count_ltail_i_r[0] +=1
                
            
            if(name_s[0] == 'ltail_i_s'):
                count_ltail_i_s[0] +=1
                


    #vertical tail



            if(name_s[0] == 'vtail'):
                if(name_s[1] == 'upp'):
                    count_vtail_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_vtail_low[0] +=1



            if(name_s[0] == 'vtail_t'):
                count_vtail_t[0] +=1
                


    #internal components

            if(name_s[0] == 'vtail_i_r'):
                count_vtail_i_r[0] +=1
                
            
            if(name_s[0] == 'vtail_i_s'):
                count_vtail_i_s[0] +=1
                
            
            

    #component intersection

            if(name_s[0] == 'lwing_fuse'):
                count_lwing_fuse[0] +=1
                

            if(name_s[0] == 'ltail_fuse'):
                count_ltail_fuse[0] +=1
                

            if(name_s[0] == 'vtail_fuse'):
                count_vtail_fuse[0] +=1
                

    #internal

            if(name_s[0] == 'lwing_Misc_1'):
                count_lwing_Misc_1[0] +=1
                
            
            if(name_s[0] == 'lwing_Misc_2'):
                count_lwing_Misc_2[0] +=1
                
            
            if(name_s[0] == 'lwing_Misc_3'):
                count_lwing_Misc_3[0] +=1
                

            if(name_s[0] == 'lwing_Misc_4'):
                count_lwing_Misc_4[0] +=1
                
        
            if(name_s[0] == 'lwing_Misc_5'):
                count_lwing_Misc_5[0] +=1
                
            
            if(name_s[0] == 'lwing_Misc_6'):
                count_lwing_Misc_6[0] +=1
                
            
            if(name_s[0] == 'ltail_Misc_1'):
                count_ltail_Misc_1[0] +=1
                
            
            if(name_s[0] == 'ltail_Misc_2'):
                count_ltail_Misc_2[0] +=1
                
            
            if(name_s[0] == 'ltail_Misc_3'):
                count_ltail_Misc_3[0] +=1
                

            if(name_s[0] == 'fus_Misc_1'):
                count_fus_Misc_1[0] +=1
                

            if(name_s[0] == 'fus_Misc_2'):
                count_fus_Misc_2[0] +=1
                



    #--------------------for strut braced wings------------------------

    #horizontal tail
                
            if(name_s[0] == 'lstrut'):
                if(name_s[1] == 'upp'):
                    count_lstrut_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_lstrut_low[0] +=1

                
            

            if(name_s[0] == 'lstrut_t'):
                count_lstrut_t[0] +=1
                


        #internal components

            if(name_s[0] == 'lstrut_i_r'):
                count_lstrut_i_r[0] +=1
                
            
            if(name_s[0] == 'lstrut_i_s'):
                count_lstrut_i_s[0] +=1
                


    #vertical tail



            if(name_s[0] == 'lv'):
                if(name_s[1] == 'upp'):
                    count_lv_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_lv_low[0] +=1



            if(name_s[0] == 'lv_t'):
                count_lv_t[0] +=1
                


    #internal components

            if(name_s[0] == 'lv_i_r'):
                count_lv_i_r[0] +=1
                
            
            if(name_s[0] == 'lv_i_s'):
                count_lv_i_s[0] +=1





    #--------2nd loop to separate and group----------------------------





        

    #store the shell elements in a map
        #based on the tags combine the elements

        local_denom = 0
        for i in range(0,len(shell_element_list)):
            name = shell_element_list[i].name
            name_s = name.split(':')
            local_i = int(name_s[2])
            local_j_list = str(name_s[3]).split('/')
            local_j = int(local_j_list[0])


    #fuselage

            if(name_s[0] == 'fuse'):
                if(name_s[1] =='top'):
                    
                    local_denom = math.ceil(count_fuse_top[0]/count_fuse_top[4])

                    
                    element_map[i] = new_element_map[int(count_fuse_top[3]+math.floor(count_fuse_top[5]/local_denom ))]
                #element_map[i] = new_element_map[int(count_fuse_top[3]+[min(math.floor(local_i/local_denom ),count_fuse_top[4]-1)])]
                    count_fuse_top[5]+=1


                
                elif(name_s[1] =='lft'):
                    
                    local_denom = math.ceil(count_fuse_lft[0]/count_fuse_lft[4])
                    element_map[i] = new_element_map[int(count_fuse_lft[3]+math.floor(count_fuse_lft[5]/local_denom ))]
                    count_fuse_lft[5]+=1
                
                elif(name_s[1] =='rght'):
                    local_denom = math.ceil(count_fuse_rght[0]/count_fuse_rght[4])
                    element_map[i] = new_element_map[int(count_fuse_rght[3]+math.floor(count_fuse_rght[5]/local_denom ))]
                    count_fuse_rght[5]+=1

                
                elif(name_s[1] =='bot'):
                    local_denom = math.ceil(count_fuse_bot[0]/count_fuse_bot[4])
                    element_map[i] = new_element_map[int(count_fuse_bot[3]+math.floor(count_fuse_bot[5]/local_denom ))]
                    count_fuse_bot[5]+=1

            
            if(name_s[0] == 'fuse_r'):
                local_denom = math.ceil(count_fuse_r[0]/count_fuse_r[4])
                element_map[i] = new_element_map[int(count_fuse_r[3]+math.floor(count_fuse_r[5]/local_denom ))]
                count_fuse_r[5]+=1

            
            if(name_s[0] == 'fuse_f'):
                local_denom = math.ceil(count_fuse_f[0]/count_fuse_f[4])
                element_map[i] = new_element_map[int(count_fuse_f[3]+math.floor(count_fuse_f[5]/local_denom ))]
                count_fuse_f[5]+=1

            
            
        #internal components
        
            if(name_s[0] == 'fus_i_r1'):
                local_denom = math.ceil(count_fus_i_r1[0]/count_fus_i_r1[4])
                element_map[i] = new_element_map[int(count_fus_i_r1[3]+math.floor(count_fus_i_r1[5]/local_denom ))]
                count_fus_i_r1[5]+=1

            
            if(name_s[0] == 'fus_i_r2'):
                local_denom = math.ceil(count_fus_i_r2[0]/count_fus_i_r2[4])
                element_map[i] = new_element_map[int(count_fus_i_r2[3]+math.floor(count_fus_i_r2[5]/local_denom ))]
                count_fus_i_r2[5]+=1

            
            if(name_s[0] == 'fus_i_r3'):
                local_denom = math.ceil(count_fus_i_r3[0]/count_fus_i_r3[4])
                element_map[i] = new_element_map[int(count_fus_i_r3[3]+math.floor(count_fus_i_r3[5]/local_denom ))]
                count_fus_i_r3[5]+=1


            if(name_s[0] == 'fus_i_r4'):
                local_denom = math.ceil(count_fus_i_r4[0]/count_fus_i_r4[4])
                element_map[i] = new_element_map[int(count_fus_i_r4[3]+math.floor(count_fus_i_r4[5]/local_denom ))]
                count_fus_i_r4[5]+=1



            if(name_s[0] == 'fus_i_l1'):
                local_denom = math.ceil(count_fus_i_l1[0]/count_fus_i_l1[4])
                element_map[i] = new_element_map[int(count_fus_i_l1[3]+math.floor(count_fus_i_l1[5]/local_denom ))]
                count_fus_i_l1[5]+=1

            
            if(name_s[0] == 'fus_i_l2'):
                local_denom = math.ceil(count_fus_i_l2[0]/count_fus_i_l2[4])
                element_map[i] = new_element_map[int(count_fus_i_l2[3]+math.floor(count_fus_i_l2[5]/local_denom ))]
                count_fus_i_l2[5]+=1

            
            if(name_s[0] == 'fus_i_l3'):
                local_denom = math.ceil(count_fus_i_l3[0]/count_fus_i_l3[4])
                element_map[i] = new_element_map[int(count_fus_i_l3[3]+math.floor(count_fus_i_l3[5]/local_denom ))]
                count_fus_i_l3[5]+=1



            if(name_s[0] == 'fus_i_l4'):
                local_denom = math.ceil(count_fus_i_l4[0]/count_fus_i_l4[4])
                element_map[i] = new_element_map[int(count_fus_i_l4[3]+math.floor(count_fus_i_l4[5]/local_denom ))]
                count_fus_i_l4[5]+=1

            
            
    #main wing
            
            if(name_s[0] == 'lwing'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_lwing_upp[0]/count_lwing_upp[4])
                    element_map[i] = new_element_map[int(count_lwing_upp[3]+math.floor(count_lwing_upp[5]/local_denom ))]
                    count_lwing_upp[5]+=1

                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_lwing_low[0]/count_lwing_low[4])
                    element_map[i] = new_element_map[int(count_lwing_low[3]+math.floor(count_lwing_low[5]/local_denom ))]
                    count_lwing_low[5]+=1

            
            if(name_s[0] == 'lwing_t'):
                local_denom = math.ceil(count_lwing_t[0]/count_lwing_t[4])
                element_map[i] = new_element_map[int(count_lwing_t[3]+math.floor(count_lwing_t[5]/local_denom ))]
                count_lwing_t[5]+=1



        #internal components

            if(name_s[0] == 'lwing_i_r'):
                local_denom = math.ceil(count_lwing_i_r[0]/count_lwing_i_r[4])
                element_map[i] = new_element_map[int(count_lwing_i_r[3]+math.floor(count_lwing_i_r[5]/local_denom ))]
                count_lwing_i_r[5]+=1


            if(name_s[0] == 'lwing_i_s'):
                local_denom = math.ceil(count_lwing_i_s[0]/count_lwing_i_s[4])
                element_map[i] = new_element_map[int(count_lwing_i_s[3]+math.floor(count_lwing_i_s[5]/local_denom ))]
                count_lwing_i_s[5]+=1

            
            if(name_s[0] == 'lwing_i_sa'):
                local_denom = math.ceil(count_lwing_i_sa[0]/count_lwing_i_sa[4])
                element_map[i] = new_element_map[int(count_lwing_i_sa[3]+math.floor(count_lwing_i_sa[5]/local_denom ))]
                count_lwing_i_sa[5]+=1

            
            if(name_s[0] == 'lwing_i_sb'):
                local_denom = math.ceil(count_lwing_i_sb[0]/count_lwing_i_sb[4])
                element_map[i] = new_element_map[int(count_lwing_i_sb[3]+math.floor( count_lwing_i_sb[5]/local_denom ))]
                count_lwing_i_sb[5]+=1

            
            if(name_s[0] == 'lwing_i_i1'):
                local_denom = math.ceil(count_lwing_i_i1[0]/count_lwing_i_i1[4])
                element_map[i] = new_element_map[int(count_lwing_i_i1[3]+math.floor(count_lwing_i_i1[5]/local_denom ))]
                count_lwing_i_i1[5]+=1


            if(name_s[0] == 'lwing_i_i2'):
                local_denom = math.ceil(count_lwing_i_i2[0]/count_lwing_i_i2[4])
                element_map[i] = new_element_map[int(count_lwing_i_i2[3]+math.floor(count_lwing_i_i2[5]/local_denom ))]
                count_lwing_i_i2[5]+=1


    #horizontal tail

            if(name_s[0] == 'ltail'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_ltail_upp[0]/count_ltail_upp[4])
                    element_map[i] = new_element_map[int(count_ltail_upp[3]+math.floor(count_ltail_upp[5]/local_denom ))]
                    count_ltail_upp[5] +=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_ltail_low[0]/count_ltail_low[4])
                    element_map[i] = new_element_map[int(count_ltail_low[3]+math.floor(count_ltail_low[5]/local_denom ))]
                    count_ltail_low[5]+=1

            

            if(name_s[0] == 'ltail_t'):
                local_denom = math.ceil(count_ltail_t[0]/count_ltail_t[4])
                element_map[i] = new_element_map[int(count_ltail_t[3]+math.floor(count_ltail_t[5]/local_denom ))]
                count_ltail_t[5]+=1


        #internal components

            if(name_s[0] == 'ltail_i_r'):
                local_denom = math.ceil(count_ltail_i_r[0]/count_ltail_i_r[4])
                element_map[i] = new_element_map[int(count_ltail_i_r[3]+math.floor(count_ltail_i_r[5]/local_denom ))]
                count_ltail_i_r[5]+=1
            
            if(name_s[0] == 'ltail_i_s'):
                local_denom = math.ceil(count_ltail_i_s[0]/count_ltail_i_s[4])
                element_map[i] = new_element_map[int(count_ltail_i_s[3]+math.floor(count_ltail_i_s[5]/local_denom ))]
                count_ltail_i_s[5]+=1


    #vertical tail



            if(name_s[0] == 'vtail'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_vtail_upp[0]/count_vtail_upp[4])
                    element_map[i] = new_element_map[int(count_vtail_upp[3]+math.floor(count_vtail_upp[5]/local_denom ))]
                    count_vtail_upp[5]+=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_vtail_low[0]/count_vtail_low[4])
                    element_map[i] = new_element_map[int(count_vtail_low[3]+math.floor(count_vtail_low[5]/local_denom ))]
                    count_vtail_low[5]+=1



            if(name_s[0] == 'vtail_t'):
                local_denom = math.ceil(count_vtail_t[0]/count_vtail_t[4])
                element_map[i] = new_element_map[int(count_vtail_t[3]+math.floor(count_vtail_t[5]/local_denom ))]
                count_vtail_t[5]+=1


    #internal components

            if(name_s[0] == 'vtail_i_r'):
                local_denom = math.ceil(count_vtail_i_r[0]/count_vtail_i_r[4])
                element_map[i] = new_element_map[int(count_vtail_i_r[3]+math.floor(count_vtail_i_r[5]/local_denom ))]
                count_vtail_i_r[5]+=1
            
            if(name_s[0] == 'vtail_i_s'):
                local_denom = math.ceil(count_vtail_i_s[0]/count_vtail_i_s[4])
                element_map[i] = new_element_map[int(count_vtail_i_s[3]+math.floor(count_vtail_i_s[5]/local_denom ))]
                count_vtail_i_s[5]+=1
            
            

    #component intersection

            if(name_s[0] == 'lwing_fuse'):
                local_denom = math.ceil(count_lwing_fuse[0]/count_lwing_fuse[4])
                element_map[i] = new_element_map[int(count_lwing_fuse[3]+math.floor(count_lwing_fuse[5]/local_denom ))]
                count_lwing_fuse[5]+=1

            if(name_s[0] == 'ltail_fuse'):
                local_denom = math.ceil(count_ltail_fuse[0]/count_ltail_fuse[4])
                element_map[i] = new_element_map[int(count_ltail_fuse[3]+math.floor(count_ltail_fuse[5]/local_denom ))]
                count_ltail_fuse[5]+=1

            if(name_s[0] == 'vtail_fuse'):
                local_denom = math.ceil(count_vtail_fuse[0]/count_vtail_fuse[4])
                element_map[i] = new_element_map[int(count_vtail_fuse[3]+math.floor(count_vtail_fuse[5]/local_denom ))]
                count_vtail_fuse[5]+=1

    #internal

            if(name_s[0] == 'lwing_Misc_1'):
                local_denom = math.ceil(count_lwing_Misc_1[0]/count_lwing_Misc_1[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_1[3]+math.floor(count_lwing_Misc_1[5]/local_denom ))]
                count_lwing_Misc_1[5]+=1
            
            if(name_s[0] == 'lwing_Misc_2'):
                local_denom = math.ceil(count_lwing_Misc_2[0]/count_lwing_Misc_2[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_2[3]+math.floor(count_lwing_Misc_2[5]/local_denom ))]
                count_lwing_Misc_2[5]+=1
            
            if(name_s[0] == 'lwing_Misc_3'):
                local_denom = math.ceil(count_lwing_Misc_3[0]/count_lwing_Misc_3[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_3[3]+math.floor(count_lwing_Misc_3[5]/local_denom ))]
                count_lwing_Misc_3[5]+=1

            if(name_s[0] == 'lwing_Misc_4'):
                local_denom = math.ceil(count_lwing_Misc_4[0]/count_lwing_Misc_4[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_4[3]+math.floor(count_lwing_Misc_4[5]/local_denom ))]
                count_lwing_Misc_4[5]+=1
        
            if(name_s[0] == 'lwing_Misc_5'):
                local_denom = math.ceil(count_lwing_Misc_5[0]/count_lwing_Misc_5[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_5[3]+math.floor(count_lwing_Misc_5[5]/local_denom ))]
                count_lwing_Misc_5[5]+=1
            
            if(name_s[0] == 'lwing_Misc_6'):
                local_denom = math.ceil(count_lwing_Misc_6[0]/count_lwing_Misc_6[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_6[3]+math.floor(count_lwing_Misc_6[5]/local_denom ))]
                count_lwing_Misc_6[5]+=1
            
            if(name_s[0] == 'ltail_Misc_1'):
                local_denom = math.ceil(count_ltail_Misc_1[0]/count_ltail_Misc_1[4])
                element_map[i] = new_element_map[int(count_ltail_Misc_1[3]+math.floor(count_ltail_Misc_[5]/local_denom ))]
                count_ltail_Misc_[5]+=1
            
            if(name_s[0] == 'ltail_Misc_2'):
                local_denom = math.ceil(count_ltail_Misc_2[0]/count_ltail_Misc_2[4])
                element_map[i] = new_element_map[int(count_ltail_Misc_2[3]+math.floor(count_ltail_Misc_2[5]/local_denom ))]
                count_ltail_Misc_2[5]+=1
            
            if(name_s[0] == 'ltail_Misc_3'):
                local_denom = math.ceil(count_ltail_Misc_3[0]/count_ltail_Misc_3[4])
                element_map[i] = new_element_map[int(count_ltail_Misc_3[3]+math.floor(count_ltail_Misc_3[5]/local_denom ))]
                count_ltail_Misc_3[5]+=1

            if(name_s[0] == 'fus_Misc_1'):
                local_denom = math.ceil(count_fus_Misc_1[0]/count_fus_Misc_1[4])
                element_map[i] = new_element_map[int(count_fus_Misc_1[3]+math.floor(count_fus_Misc_1[5]/local_denom ))]
                count_fus_Misc_1[5]+=1

            if(name_s[0] == 'fus_Misc_2'):
                local_denom = math.ceil(count_fus_Misc_2[0]/count_fus_Misc_2[4])
                element_map[i] = new_element_map[int(count_fus_Misc_2[3]+math.floor(count_fus_Misc_2[5]/local_denom ))]
                count_fus_Misc_2[5]+=1





    #for strut braced wings-------------------------------

                #horizontal tail
                
            if(name_s[0] == 'lstrut'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_lstrut_upp[0]/count_lstrut_upp[4])
                    element_map[i] = new_element_map[int(count_lstrut_upp[3]+math.floor(count_lstrut_upp[5]/local_denom ))]
                    count_lstrut_upp[5] +=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_lstrut_low[0]/count_lstrut_low[4])
                    element_map[i] = new_element_map[int(count_lstrut_low[3]+math.floor(count_lstrut_low[5]/local_denom ))]
                    count_lstrut_low[5]+=1

            

            if(name_s[0] == 'lstrut_t'):
                local_denom = math.ceil(count_lstrut_t[0]/count_lstrut_t[4])
                element_map[i] = new_element_map[int(count_lstrut_t[3]+math.floor(count_lstrut_t[5]/local_denom ))]
                count_lstrut_t[5]+=1


        #internal components

            if(name_s[0] == 'lstrut_i_r'):
                local_denom = math.ceil(count_lstrut_i_r[0]/count_lstrut_i_r[4])
                element_map[i] = new_element_map[int(count_lstrut_i_r[3]+math.floor(count_lstrut_i_r[5]/local_denom ))]
                count_lstrut_i_r[5]+=1
            
            if(name_s[0] == 'lstrut_i_s'):
                local_denom = math.ceil(count_lstrut_i_s[0]/count_lstrut_i_s[4])
                element_map[i] = new_element_map[int(count_lstrut_i_s[3]+math.floor(count_lstrut_i_s[5]/local_denom ))]
                count_lstrut_i_s[5]+=1


    #vertical tail



            if(name_s[0] == 'lv'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_lv_upp[0]/count_lv_upp[4])
                    element_map[i] = new_element_map[int(count_lv_upp[3]+math.floor(count_lv_upp[5]/local_denom ))]
                    count_lv_upp[5]+=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_lv_low[0]/count_lv_low[4])
                    element_map[i] = new_element_map[int(count_lv_low[3]+math.floor(count_lv_low[5]/local_denom ))]
                    count_lv_low[5]+=1



            if(name_s[0] == 'lv_t'):
                local_denom = math.ceil(count_lv_t[0]/count_lv_t[4])
                element_map[i] = new_element_map[int(count_lv_t[3]+math.floor(count_lv_t[5]/local_denom ))]
                count_lv_t[5]+=1


    #internal components

            if(name_s[0] == 'lv_i_r'):
                local_denom = math.ceil(count_lv_i_r[0]/count_lv_i_r[4])
                element_map[i] = new_element_map[int(count_lv_i_r[3]+math.floor(count_lv_i_r[5]/local_denom ))]
                count_lv_i_r[5]+=1
            
            if(name_s[0] == 'lv_i_s'):
                local_denom = math.ceil(count_lv_i_s[0]/count_lv_i_s[4])
                element_map[i] = new_element_map[int(count_lv_i_s[3]+math.floor(count_lv_i_s[5]/local_denom ))]
                count_lv_i_s[5]+=1




    elif (aircraft.type=="Strut_braced"):

        #count fuse i
        #0 - local count , 1 - i, 2 - j , 3 - placeholder
        #fuselage
        count_fuse = np.zeros(6) #0
        count_fuse_top = np.zeros(6) #0
        count_fuse_lft = np.zeros(6) #0
        count_fuse_rght = np.zeros(6) #0
        count_fuse_bot = np.zeros(6) #0
        
        count_fuse_r = np.zeros(6) #0
        count_fuse_f = np.zeros(6) #0
        count_fus_i_r1 = np.zeros(6) #0
        count_fus_i_r2 = np.zeros(6) #0
        count_fus_i_r3 = np.zeros(6) #0
        count_fus_i_r4 = np.zeros(6) #0
        count_fus_i_l1 = np.zeros(6) #0
        count_fus_i_l2 = np.zeros(6) #0
        count_fus_i_l3 = np.zeros(6) #0
        count_fus_i_l4 = np.zeros(6) #0
        
        #wings
        count_lwing = np.zeros(6) #0
        count_lwing_upp = np.zeros(6) #0
        count_lwing_low = np.zeros(6) #0
        
        count_lwing_t = np.zeros(6) #0
        count_lwing_i_r = np.zeros(6) #0
        count_lwing_i_s = np.zeros(6) #0
        count_lwing_i_sa = np.zeros(6) #0
        count_lwing_i_sb = np.zeros(6) #0
        count_lwing_i_i1 = np.zeros(6) #0
        count_lwing_i_i2 = np.zeros(6) #0
        
        #ltail
        count_ltail = np.zeros(6) #0
        count_ltail_upp = np.zeros(6) #0
        count_ltail_low = np.zeros(6) #0
        
        count_ltail_t = np.zeros(6) #0
        count_ltail_i_r = np.zeros(6) #0
        count_ltail_i_s = np.zeros(6) #0
        
        #vtail
        count_vtail = np.zeros(6) #0
        count_vtail_upp = np.zeros(6) #0
        count_vtail_low = np.zeros(6) #0
        
        
        count_vtail_t = np.zeros(6) #0
        count_vtail_i_r = np.zeros(6) #0
        count_vtail_i_s = np.zeros(6) #0
        
        #intersections
        count_lwing_fuse = np.zeros(6) #0
        count_ltail_fuse = np.zeros(6) #0
        count_vtail_fuse = np.zeros(6) #0
        
        #intersections internal
        count_lwing_Misc_1 = np.zeros(6) #0
        count_lwing_Misc_2 = np.zeros(6) #0
        count_lwing_Misc_3 = np.zeros(6) #0
        count_lwing_Misc_4 = np.zeros(6) #0
        count_lwing_Misc_5 = np.zeros(6) #0
        count_lwing_Misc_6 = np.zeros(6) #0
        count_ltail_Misc_1 = np.zeros(6) #0
        count_ltail_Misc_2 = np.zeros(6) #0
        count_ltail_Misc_3 = np.zeros(6) #0
        count_fus_Misc_1 = np.zeros(6) #0
        count_fus_Misc_2 = np.zeros(6) #0
        
        
        #for strut braced
        
        #ltail
        count_lstrut = np.zeros(6) #0
        count_lstrut_upp = np.zeros(6) #0
        count_lstrut_low = np.zeros(6) #0
        
        count_lstrut_t = np.zeros(6) #0
        count_lstrut_i_r = np.zeros(6) #0
        count_lstrut_i_s = np.zeros(6) #0
        
        #vtail
        count_lv = np.zeros(6) #0
        count_lv_upp = np.zeros(6) #0
        count_lv_low = np.zeros(6) #0
        
        
        count_lv_t = np.zeros(6) #0
        count_lv_i_r = np.zeros(6) #0
        count_lv_i_s = np.zeros(6) #0
        
        #intersections
    #    lstrut_fuse
    #    lstrut_lwing
    #    lv_lwing
    #    lv_lstrut
    #    ltail_vtail

        #------------------------------------------------------------------------------------



        #dv_breakdown.max   #if 0 then use existing breakdown, if 1, then use specified breakdown if -1, then use max breakdown i.e. all elements are desiogn variables

        #each a 2d array
        
        for i in range(0,4):
        
            count_fuse_top[i+1] = dv_breakdown.fuselage_skin_top[i]
            count_fuse_bot[i+1] = dv_breakdown.fuselage_skin_bottom[i]
            count_fuse_lft[i+1] = dv_breakdown.fuselage_skin_left[i]
            count_fuse_rght[i+1] = dv_breakdown.fuselage_skin_right[i]
            count_fuse_f[i+1] = dv_breakdown.fuselage_front[i]
            count_fuse_r[i+1] = dv_breakdown.fuselage_rear[i]
            
            count_fus_i_r1[i+1] = dv_breakdown.fuselage_internal_r1[i]
            count_fus_i_r2[i+1] = dv_breakdown.fuselage_internal_r2[i]
            count_fus_i_r3[i+1] = dv_breakdown.fuselage_internal_r3[i]
            count_fus_i_r4[i+1] = dv_breakdown.fuselage_internal_r4[i]
            
            count_fus_i_l1[i+1] = dv_breakdown.fuselage_internal_l1[i]
            count_fus_i_l2[i+1] = dv_breakdown.fuselage_internal_l2[i]
            count_fus_i_l3[i+1] = dv_breakdown.fuselage_internal_l3[i]
            count_fus_i_l4[i+1] = dv_breakdown.fuselage_internal_l4[i]
            
            
            count_lwing_upp[i+1] = dv_breakdown.lwing_upper[i]
            count_lwing_low[i+1] = dv_breakdown.lwing_lower[i]
            count_lwing_t[i+1] = dv_breakdown.lwing_tip[i]
            count_lwing_i_s[i+1] = dv_breakdown.lwing_spars_s1[i]
            count_lwing_i_sa[i+1] = dv_breakdown.lwing_spars_s2[i]
            count_lwing_i_sb[i+1] = dv_breakdown.lwing_spars_s3[i]
            count_lwing_i_r[i+1] = dv_breakdown.lwing_ribs[i]
            count_lwing_i_i1[i+1] = dv_breakdown.lwing_internal_i1[i]
            count_lwing_i_i2[i+1] = dv_breakdown.lwing_internal_i2[i]
            
            count_ltail_upp[i+1] = dv_breakdown.ltail_upper[i]
            count_ltail_low[i+1] = dv_breakdown.ltail_lower[i]
            count_ltail_t[i+1] = dv_breakdown.ltail_tip[i]
            count_ltail_i_s[i+1] = dv_breakdown.ltail_spars[i]
            count_ltail_i_r[i+1] = dv_breakdown.ltail_ribs[i]
            
            count_vtail_upp[i+1] = dv_breakdown.vtail_upper[i]
            count_vtail_low[i+1] = dv_breakdown.vtail_lower[i]
            count_vtail_t[i+1] = dv_breakdown.vtail_tip[i]
            count_vtail_i_s[i+1] = dv_breakdown.vtail_spars[i]
            count_vtail_i_r[i+1] = dv_breakdown.vtail_ribs[i]
            
            
            
            count_lwing_fuse[i+1] = dv_breakdown.intersection_lwing_fuse[i]
            count_ltail_fuse[i+1] = dv_breakdown.intersection_ltail_fuse[i]
            count_vtail_fuse[i+1] = dv_breakdown.intersection_vtail_fuse[i]
            

            count_lwing_Misc_1[i+1] = dv_breakdown.miscellaneous_w1[i]
            count_lwing_Misc_2[i+1] = dv_breakdown.miscellaneous_w2[i]
            count_lwing_Misc_3[i+1] = dv_breakdown.miscellaneous_w3[i]
            count_lwing_Misc_4[i+1] = dv_breakdown.miscellaneous_w4[i]
            count_lwing_Misc_5[i+1] = dv_breakdown.miscellaneous_w5[i]
            count_lwing_Misc_6[i+1] = dv_breakdown.miscellaneous_w6[i]
            count_ltail_Misc_1[i+1] = dv_breakdown.miscellaneous_t1[i]
            count_ltail_Misc_2[i+1] = dv_breakdown.miscellaneous_t2[i]
            count_ltail_Misc_3[i+1] = dv_breakdown.miscellaneous_t3[i]
            count_fus_Misc_1[i+1] = dv_breakdown.miscellaneous_f1[i]
            count_fus_Misc_2[i+1] = dv_breakdown.miscellaneous_f2[i]
        
        
        #for strut braced
        
            count_lstrut_low[i+1] = dv_breakdown.ltail_lower[i]
            count_lstrut_t[i+1] = dv_breakdown.ltail_tip[i]
            count_lstrut_i_s[i+1] = dv_breakdown.ltail_spars[i]
            count_lstrut_i_r[i+1] = dv_breakdown.ltail_ribs[i]
            
            count_lv_upp[i+1] = dv_breakdown.vtail_upper[i]
            count_lv_low[i+1] = dv_breakdown.vtail_lower[i]
            count_lv_t[i+1] = dv_breakdown.vtail_tip[i]
            count_lv_i_s[i+1] = dv_breakdown.vtail_spars[i]
            count_lv_i_r[i+1] = dv_breakdown.vtail_ribs[i]
        

        #class in aircraft that has the number of dvs
        no_of_dvs = dv_breakdown.total
        #dv_new = np.zeros(no_of_dvs)
        new_element_map = dv_breakdown.new_element_map
        shell_element_list_new = dv_breakdown.shell_element_list_new
        no_of_shell_elements_new = len(shell_element_list_new)
        
        

    #store the shell elements in a map
        #based on the tags combine the elements

        for i in range(0,len(shell_element_list)):
            name = shell_element_list[i].name
            name_s = name.split(':')


    #fuselage

            if(name_s[0] == 'fuse'):
                if(name_s[1] =='top'):
                    count_fuse_top[0] +=1
                
                elif(name_s[1] =='lft'):
                    count_fuse_lft[0] +=1
                
                elif(name_s[1] =='rght'):
                    count_fuse_rght[0] +=1
                
                elif(name_s[1] =='bot'):
                    count_fuse_bot[0] +=1
                
            
            if(name_s[0] == 'fuse_r'):
                count_fuse_r[0] +=1
                
            
            if(name_s[0] == 'fuse_f'):
                count_fuse_f[0] +=1
                
            
            
        #internal components
        
            if(name_s[0] == 'fus_i_r1'):
                count_fus_i_r1[0] +=1
                
            
            if(name_s[0] == 'fus_i_r2'):
                count_fus_i_r2[0] +=1
                
            
            if(name_s[0] == 'fus_i_r3'):
                count_fus_i_r3[0] +=1
                

            if(name_s[0] == 'fus_i_r4'):
                count_fus_i_r4[0] +=1
                


            if(name_s[0] == 'fus_i_l1'):
                count_fus_i_l1[0] +=1
                
            
            if(name_s[0] == 'fus_i_l2'):
                count_fus_i_l2[0] +=1
                
            
            if(name_s[0] == 'fus_i_l3'):
                count_fus_i_l3[0] +=1
                

            if(name_s[0] == 'fus_i_l4'):
                count_fus_i_l4[0] +=1
                
            
            
    #main wing
            
            if(name_s[0] == 'lwing'):
                if(name_s[1] == 'upp'):
                    count_lwing_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_lwing_low[0] +=1

                
            
            if(name_s[0] == 'lwing_t'):
                count_lwing_t[0] +=1
                


        #internal components

            if(name_s[0] == 'lwing_i_r'):
                count_lwing_i_r[0] +=1
                

            if(name_s[0] == 'lwing_i_s'):
                count_lwing_i_s[0] +=1
                
            
            if(name_s[0] == 'lwing_i_sa'):
                count_lwing_i_sa[0] +=1
                
            
            if(name_s[0] == 'lwing_i_sb'):
                count_lwing_i_sb[0] +=1
                
            
            if(name_s[0] == 'lwing_i_i1'):
                count_lwing_i_i1[0] +=1
                

            if(name_s[0] == 'lwing_i_i2'):
                count_lwing_i_i2[0] +=1
                

    #horizontal tail

            if(name_s[0] == 'ltail'):
                if(name_s[1] == 'upp'):
                    count_ltail_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_ltail_low[0] +=1

                
            

            if(name_s[0] == 'ltail_t'):
                count_ltail_t[0] +=1
                


        #internal components

            if(name_s[0] == 'ltail_i_r'):
                count_ltail_i_r[0] +=1
                
            
            if(name_s[0] == 'ltail_i_s'):
                count_ltail_i_s[0] +=1
                


    #vertical tail



            if(name_s[0] == 'vtail'):
                if(name_s[1] == 'upp'):
                    count_vtail_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_vtail_low[0] +=1



            if(name_s[0] == 'vtail_t'):
                count_vtail_t[0] +=1
                


    #internal components

            if(name_s[0] == 'vtail_i_r'):
                count_vtail_i_r[0] +=1
                
            
            if(name_s[0] == 'vtail_i_s'):
                count_vtail_i_s[0] +=1
                
            
            

    #component intersection

            if(name_s[0] == 'lwing_fuse'):
                count_lwing_fuse[0] +=1
                

            if(name_s[0] == 'ltail_fuse'):
                count_ltail_fuse[0] +=1
                

            if(name_s[0] == 'vtail_fuse'):
                count_vtail_fuse[0] +=1
                

    #internal

            if(name_s[0] == 'lwing_Misc_1'):
                count_lwing_Misc_1[0] +=1
                
            
            if(name_s[0] == 'lwing_Misc_2'):
                count_lwing_Misc_2[0] +=1
                
            
            if(name_s[0] == 'lwing_Misc_3'):
                count_lwing_Misc_3[0] +=1
                

            if(name_s[0] == 'lwing_Misc_4'):
                count_lwing_Misc_4[0] +=1
                
        
            if(name_s[0] == 'lwing_Misc_5'):
                count_lwing_Misc_5[0] +=1
                
            
            if(name_s[0] == 'lwing_Misc_6'):
                count_lwing_Misc_6[0] +=1
                
            
            if(name_s[0] == 'ltail_Misc_1'):
                count_ltail_Misc_1[0] +=1
                
            
            if(name_s[0] == 'ltail_Misc_2'):
                count_ltail_Misc_2[0] +=1
                
            
            if(name_s[0] == 'ltail_Misc_3'):
                count_ltail_Misc_3[0] +=1
                

            if(name_s[0] == 'fus_Misc_1'):
                count_fus_Misc_1[0] +=1
                

            if(name_s[0] == 'fus_Misc_2'):
                count_fus_Misc_2[0] +=1
                



    #--------------------for strut braced wings------------------------

    #horizontal tail
                
            if(name_s[0] == 'lstrut'):
                if(name_s[1] == 'upp'):
                    count_lstrut_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_lstrut_low[0] +=1

                
            

            if(name_s[0] == 'lstrut_t'):
                count_lstrut_t[0] +=1
                


        #internal components

            if(name_s[0] == 'lstrut_i_r'):
                count_lstrut_i_r[0] +=1
                
            
            if(name_s[0] == 'lstrut_i_s'):
                count_lstrut_i_s[0] +=1
                


    #vertical tail



            if(name_s[0] == 'lv'):
                if(name_s[1] == 'upp'):
                    count_lv_upp[0] +=1
                
                elif(name_s[1] == 'low'):
                    count_lv_low[0] +=1



            if(name_s[0] == 'lv_t'):
                count_lv_t[0] +=1
                


    #internal components

            if(name_s[0] == 'lv_i_r'):
                count_lv_i_r[0] +=1
                
            
            if(name_s[0] == 'lv_i_s'):
                count_lv_i_s[0] +=1





    #--------2nd loop to separate and group----------------------------





        

    #store the shell elements in a map
        #based on the tags combine the elements

        local_denom = 0
        for i in range(0,len(shell_element_list)):
            name = shell_element_list[i].name
            name_s = name.split(':')
            local_i = int(name_s[2])
            local_j_list = str(name_s[3]).split('/')
            local_j = int(local_j_list[0])


    #fuselage

            if(name_s[0] == 'fuse'):
                if(name_s[1] =='top'):
                    
                    local_denom = math.ceil(count_fuse_top[0]/count_fuse_top[4])

                    
                    element_map[i] = new_element_map[int(count_fuse_top[3]+math.floor(count_fuse_top[5]/local_denom ))]
                #element_map[i] = new_element_map[int(count_fuse_top[3]+[min(math.floor(local_i/local_denom ),count_fuse_top[4]-1)])]
                    count_fuse_top[5]+=1


                
                elif(name_s[1] =='lft'):
                    
                    local_denom = math.ceil(count_fuse_lft[0]/count_fuse_lft[4])
                    element_map[i] = new_element_map[int(count_fuse_lft[3]+math.floor(count_fuse_lft[5]/local_denom ))]
                    count_fuse_lft[5]+=1
                
                elif(name_s[1] =='rght'):
                    local_denom = math.ceil(count_fuse_rght[0]/count_fuse_rght[4])
                    element_map[i] = new_element_map[int(count_fuse_rght[3]+math.floor(count_fuse_rght[5]/local_denom ))]
                    count_fuse_rght[5]+=1

                
                elif(name_s[1] =='bot'):
                    local_denom = math.ceil(count_fuse_bot[0]/count_fuse_bot[4])
                    element_map[i] = new_element_map[int(count_fuse_bot[3]+math.floor(count_fuse_bot[5]/local_denom ))]
                    count_fuse_bot[5]+=1

            
            if(name_s[0] == 'fuse_r'):
                local_denom = math.ceil(count_fuse_r[0]/count_fuse_r[4])
                element_map[i] = new_element_map[int(count_fuse_r[3]+math.floor(count_fuse_r[5]/local_denom ))]
                count_fuse_r[5]+=1

            
            if(name_s[0] == 'fuse_f'):
                local_denom = math.ceil(count_fuse_f[0]/count_fuse_f[4])
                element_map[i] = new_element_map[int(count_fuse_f[3]+math.floor(count_fuse_f[5]/local_denom ))]
                count_fuse_f[5]+=1

            
            
        #internal components
        
            if(name_s[0] == 'fus_i_r1'):
                local_denom = math.ceil(count_fus_i_r1[0]/count_fus_i_r1[4])
                element_map[i] = new_element_map[int(count_fus_i_r1[3]+math.floor(count_fus_i_r1[5]/local_denom ))]
                count_fus_i_r1[5]+=1

            
            if(name_s[0] == 'fus_i_r2'):
                local_denom = math.ceil(count_fus_i_r2[0]/count_fus_i_r2[4])
                element_map[i] = new_element_map[int(count_fus_i_r2[3]+math.floor(count_fus_i_r2[5]/local_denom ))]
                count_fus_i_r2[5]+=1

            
            if(name_s[0] == 'fus_i_r3'):
                local_denom = math.ceil(count_fus_i_r3[0]/count_fus_i_r3[4])
                element_map[i] = new_element_map[int(count_fus_i_r3[3]+math.floor(count_fus_i_r3[5]/local_denom ))]
                count_fus_i_r3[5]+=1


            if(name_s[0] == 'fus_i_r4'):
                local_denom = math.ceil(count_fus_i_r4[0]/count_fus_i_r4[4])
                element_map[i] = new_element_map[int(count_fus_i_r4[3]+math.floor(count_fus_i_r4[5]/local_denom ))]
                count_fus_i_r4[5]+=1



            if(name_s[0] == 'fus_i_l1'):
                local_denom = math.ceil(count_fus_i_l1[0]/count_fus_i_l1[4])
                element_map[i] = new_element_map[int(count_fus_i_l1[3]+math.floor(count_fus_i_l1[5]/local_denom ))]
                count_fus_i_l1[5]+=1

            
            if(name_s[0] == 'fus_i_l2'):
                local_denom = math.ceil(count_fus_i_l2[0]/count_fus_i_l2[4])
                element_map[i] = new_element_map[int(count_fus_i_l2[3]+math.floor(count_fus_i_l2[5]/local_denom ))]
                count_fus_i_l2[5]+=1

            
            if(name_s[0] == 'fus_i_l3'):
                local_denom = math.ceil(count_fus_i_l3[0]/count_fus_i_l3[4])
                element_map[i] = new_element_map[int(count_fus_i_l3[3]+math.floor(count_fus_i_l3[5]/local_denom ))]
                count_fus_i_l3[5]+=1



            if(name_s[0] == 'fus_i_l4'):
                local_denom = math.ceil(count_fus_i_l4[0]/count_fus_i_l4[4])
                element_map[i] = new_element_map[int(count_fus_i_l4[3]+math.floor(count_fus_i_l4[5]/local_denom ))]
                count_fus_i_l4[5]+=1

            
            
    #main wing
            
            if(name_s[0] == 'lwing'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_lwing_upp[0]/count_lwing_upp[4])
                    element_map[i] = new_element_map[int(count_lwing_upp[3]+math.floor(count_lwing_upp[5]/local_denom ))]
                    count_lwing_upp[5]+=1

                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_lwing_low[0]/count_lwing_low[4])
                    element_map[i] = new_element_map[int(count_lwing_low[3]+math.floor(count_lwing_low[5]/local_denom ))]
                    count_lwing_low[5]+=1

            
            if(name_s[0] == 'lwing_t'):
                local_denom = math.ceil(count_lwing_t[0]/count_lwing_t[4])
                element_map[i] = new_element_map[int(count_lwing_t[3]+math.floor(count_lwing_t[5]/local_denom ))]
                count_lwing_t[5]+=1



        #internal components

            if(name_s[0] == 'lwing_i_r'):
                local_denom = math.ceil(count_lwing_i_r[0]/count_lwing_i_r[4])
                element_map[i] = new_element_map[int(count_lwing_i_r[3]+math.floor(count_lwing_i_r[5]/local_denom ))]
                count_lwing_i_r[5]+=1


            if(name_s[0] == 'lwing_i_s'):
                local_denom = math.ceil(count_lwing_i_s[0]/count_lwing_i_s[4])
                element_map[i] = new_element_map[int(count_lwing_i_s[3]+math.floor(count_lwing_i_s[5]/local_denom ))]
                count_lwing_i_s[5]+=1

            
            if(name_s[0] == 'lwing_i_sa'):
                local_denom = math.ceil(count_lwing_i_sa[0]/count_lwing_i_sa[4])
                element_map[i] = new_element_map[int(count_lwing_i_sa[3]+math.floor(count_lwing_i_sa[5]/local_denom ))]
                count_lwing_i_sa[5]+=1

            
            if(name_s[0] == 'lwing_i_sb'):
                local_denom = math.ceil(count_lwing_i_sb[0]/count_lwing_i_sb[4])
                element_map[i] = new_element_map[int(count_lwing_i_sb[3]+math.floor( count_lwing_i_sb[5]/local_denom ))]
                count_lwing_i_sb[5]+=1

            
            if(name_s[0] == 'lwing_i_i1'):
                local_denom = math.ceil(count_lwing_i_i1[0]/count_lwing_i_i1[4])
                element_map[i] = new_element_map[int(count_lwing_i_i1[3]+math.floor(count_lwing_i_i1[5]/local_denom ))]
                count_lwing_i_i1[5]+=1


            if(name_s[0] == 'lwing_i_i2'):
                local_denom = math.ceil(count_lwing_i_i2[0]/count_lwing_i_i2[4])
                element_map[i] = new_element_map[int(count_lwing_i_i2[3]+math.floor(count_lwing_i_i2[5]/local_denom ))]
                count_lwing_i_i2[5]+=1


    #horizontal tail

            if(name_s[0] == 'ltail'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_ltail_upp[0]/count_ltail_upp[4])
                    element_map[i] = new_element_map[int(count_ltail_upp[3]+math.floor(count_ltail_upp[5]/local_denom ))]
                    count_ltail_upp[5] +=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_ltail_low[0]/count_ltail_low[4])
                    element_map[i] = new_element_map[int(count_ltail_low[3]+math.floor(count_ltail_low[5]/local_denom ))]
                    count_ltail_low[5]+=1

            

            if(name_s[0] == 'ltail_t'):
                local_denom = math.ceil(count_ltail_t[0]/count_ltail_t[4])
                element_map[i] = new_element_map[int(count_ltail_t[3]+math.floor(count_ltail_t[5]/local_denom ))]
                count_ltail_t[5]+=1


        #internal components

            if(name_s[0] == 'ltail_i_r'):
                local_denom = math.ceil(count_ltail_i_r[0]/count_ltail_i_r[4])
                element_map[i] = new_element_map[int(count_ltail_i_r[3]+math.floor(count_ltail_i_r[5]/local_denom ))]
                count_ltail_i_r[5]+=1
            
            if(name_s[0] == 'ltail_i_s'):
                local_denom = math.ceil(count_ltail_i_s[0]/count_ltail_i_s[4])
                element_map[i] = new_element_map[int(count_ltail_i_s[3]+math.floor(count_ltail_i_s[5]/local_denom ))]
                count_ltail_i_s[5]+=1


    #vertical tail



            if(name_s[0] == 'vtail'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_vtail_upp[0]/count_vtail_upp[4])
                    element_map[i] = new_element_map[int(count_vtail_upp[3]+math.floor(count_vtail_upp[5]/local_denom ))]
                    count_vtail_upp[5]+=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_vtail_low[0]/count_vtail_low[4])
                    element_map[i] = new_element_map[int(count_vtail_low[3]+math.floor(count_vtail_low[5]/local_denom ))]
                    count_vtail_low[5]+=1



            if(name_s[0] == 'vtail_t'):
                local_denom = math.ceil(count_vtail_t[0]/count_vtail_t[4])
                element_map[i] = new_element_map[int(count_vtail_t[3]+math.floor(count_vtail_t[5]/local_denom ))]
                count_vtail_t[5]+=1


    #internal components

            if(name_s[0] == 'vtail_i_r'):
                local_denom = math.ceil(count_vtail_i_r[0]/count_vtail_i_r[4])
                element_map[i] = new_element_map[int(count_vtail_i_r[3]+math.floor(count_vtail_i_r[5]/local_denom ))]
                count_vtail_i_r[5]+=1
            
            if(name_s[0] == 'vtail_i_s'):
                local_denom = math.ceil(count_vtail_i_s[0]/count_vtail_i_s[4])
                element_map[i] = new_element_map[int(count_vtail_i_s[3]+math.floor(count_vtail_i_s[5]/local_denom ))]
                count_vtail_i_s[5]+=1
            
            

    #component intersection

            if(name_s[0] == 'lwing_fuse'):
                local_denom = math.ceil(count_lwing_fuse[0]/count_lwing_fuse[4])
                element_map[i] = new_element_map[int(count_lwing_fuse[3]+math.floor(count_lwing_fuse[5]/local_denom ))]
                count_lwing_fuse[5]+=1

            if(name_s[0] == 'ltail_fuse'):
                local_denom = math.ceil(count_ltail_fuse[0]/count_ltail_fuse[4])
                element_map[i] = new_element_map[int(count_ltail_fuse[3]+math.floor(count_ltail_fuse[5]/local_denom ))]
                count_ltail_fuse[5]+=1

            if(name_s[0] == 'vtail_fuse'):
                local_denom = math.ceil(count_vtail_fuse[0]/count_vtail_fuse[4])
                element_map[i] = new_element_map[int(count_vtail_fuse[3]+math.floor(count_vtail_fuse[5]/local_denom ))]
                count_vtail_fuse[5]+=1

    #internal

            if(name_s[0] == 'lwing_Misc_1'):
                local_denom = math.ceil(count_lwing_Misc_1[0]/count_lwing_Misc_1[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_1[3]+math.floor(count_lwing_Misc_1[5]/local_denom ))]
                count_lwing_Misc_1[5]+=1
            
            if(name_s[0] == 'lwing_Misc_2'):
                local_denom = math.ceil(count_lwing_Misc_2[0]/count_lwing_Misc_2[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_2[3]+math.floor(count_lwing_Misc_2[5]/local_denom ))]
                count_lwing_Misc_2[5]+=1
            
            if(name_s[0] == 'lwing_Misc_3'):
                local_denom = math.ceil(count_lwing_Misc_3[0]/count_lwing_Misc_3[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_3[3]+math.floor(count_lwing_Misc_3[5]/local_denom ))]
                count_lwing_Misc_3[5]+=1

            if(name_s[0] == 'lwing_Misc_4'):
                local_denom = math.ceil(count_lwing_Misc_4[0]/count_lwing_Misc_4[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_4[3]+math.floor(count_lwing_Misc_4[5]/local_denom ))]
                count_lwing_Misc_4[5]+=1
        
            if(name_s[0] == 'lwing_Misc_5'):
                local_denom = math.ceil(count_lwing_Misc_5[0]/count_lwing_Misc_5[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_5[3]+math.floor(count_lwing_Misc_5[5]/local_denom ))]
                count_lwing_Misc_5[5]+=1
            
            if(name_s[0] == 'lwing_Misc_6'):
                local_denom = math.ceil(count_lwing_Misc_6[0]/count_lwing_Misc_6[4])
                element_map[i] = new_element_map[int(count_lwing_Misc_6[3]+math.floor(count_lwing_Misc_6[5]/local_denom ))]
                count_lwing_Misc_6[5]+=1
            
            if(name_s[0] == 'ltail_Misc_1'):
                local_denom = math.ceil(count_ltail_Misc_1[0]/count_ltail_Misc_1[4])
                element_map[i] = new_element_map[int(count_ltail_Misc_1[3]+math.floor(count_ltail_Misc_[5]/local_denom ))]
                count_ltail_Misc_[5]+=1
            
            if(name_s[0] == 'ltail_Misc_2'):
                local_denom = math.ceil(count_ltail_Misc_2[0]/count_ltail_Misc_2[4])
                element_map[i] = new_element_map[int(count_ltail_Misc_2[3]+math.floor(count_ltail_Misc_2[5]/local_denom ))]
                count_ltail_Misc_2[5]+=1
            
            if(name_s[0] == 'ltail_Misc_3'):
                local_denom = math.ceil(count_ltail_Misc_3[0]/count_ltail_Misc_3[4])
                element_map[i] = new_element_map[int(count_ltail_Misc_3[3]+math.floor(count_ltail_Misc_3[5]/local_denom ))]
                count_ltail_Misc_3[5]+=1

            if(name_s[0] == 'fus_Misc_1'):
                local_denom = math.ceil(count_fus_Misc_1[0]/count_fus_Misc_1[4])
                element_map[i] = new_element_map[int(count_fus_Misc_1[3]+math.floor(count_fus_Misc_1[5]/local_denom ))]
                count_fus_Misc_1[5]+=1

            if(name_s[0] == 'fus_Misc_2'):
                local_denom = math.ceil(count_fus_Misc_2[0]/count_fus_Misc_2[4])
                element_map[i] = new_element_map[int(count_fus_Misc_2[3]+math.floor(count_fus_Misc_2[5]/local_denom ))]
                count_fus_Misc_2[5]+=1





    #for strut braced wings-------------------------------

                #horizontal tail
                
            if(name_s[0] == 'lstrut'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_lstrut_upp[0]/count_lstrut_upp[4])
                    element_map[i] = new_element_map[int(count_lstrut_upp[3]+math.floor(count_lstrut_upp[5]/local_denom ))]
                    count_lstrut_upp[5] +=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_lstrut_low[0]/count_lstrut_low[4])
                    element_map[i] = new_element_map[int(count_lstrut_low[3]+math.floor(count_lstrut_low[5]/local_denom ))]
                    count_lstrut_low[5]+=1

            

            if(name_s[0] == 'lstrut_t'):
                local_denom = math.ceil(count_lstrut_t[0]/count_lstrut_t[4])
                element_map[i] = new_element_map[int(count_lstrut_t[3]+math.floor(count_lstrut_t[5]/local_denom ))]
                count_lstrut_t[5]+=1


        #internal components

            if(name_s[0] == 'lstrut_i_r'):
                local_denom = math.ceil(count_lstrut_i_r[0]/count_lstrut_i_r[4])
                element_map[i] = new_element_map[int(count_lstrut_i_r[3]+math.floor(count_lstrut_i_r[5]/local_denom ))]
                count_lstrut_i_r[5]+=1
            
            if(name_s[0] == 'lstrut_i_s'):
                local_denom = math.ceil(count_lstrut_i_s[0]/count_lstrut_i_s[4])
                element_map[i] = new_element_map[int(count_lstrut_i_s[3]+math.floor(count_lstrut_i_s[5]/local_denom ))]
                count_lstrut_i_s[5]+=1


    #vertical tail



            if(name_s[0] == 'lv'):
                if(name_s[1] == 'upp'):
                    local_denom = math.ceil(count_lv_upp[0]/count_lv_upp[4])
                    element_map[i] = new_element_map[int(count_lv_upp[3]+math.floor(count_lv_upp[5]/local_denom ))]
                    count_lv_upp[5]+=1
                
                elif(name_s[1] == 'low'):
                    local_denom = math.ceil(count_lv_low[0]/count_lv_low[4])
                    element_map[i] = new_element_map[int(count_lv_low[3]+math.floor(count_lv_low[5]/local_denom ))]
                    count_lv_low[5]+=1



            if(name_s[0] == 'lv_t'):
                local_denom = math.ceil(count_lv_t[0]/count_lv_t[4])
                element_map[i] = new_element_map[int(count_lv_t[3]+math.floor(count_lv_t[5]/local_denom ))]
                count_lv_t[5]+=1


    #internal components

            if(name_s[0] == 'lv_i_r'):
                local_denom = math.ceil(count_lv_i_r[0]/count_lv_i_r[4])
                element_map[i] = new_element_map[int(count_lv_i_r[3]+math.floor(count_lv_i_r[5]/local_denom ))]
                count_lv_i_r[5]+=1
            
            if(name_s[0] == 'lv_i_s'):
                local_denom = math.ceil(count_lv_i_s[0]/count_lv_i_s[4])
                element_map[i] = new_element_map[int(count_lv_i_s[3]+math.floor(count_lv_i_s[5]/local_denom ))]
                count_lv_i_s[5]+=1






    #rename the old file to a new file,
    os.rename(bdf_structural_meshfile, bdf_structural_meshfile+".old")


#---write a bdf file for geomach-------------------------------------------------------------------

    fo = open(bdf_structural_meshfile,"wb")
    #---------Executive_control_section----------------------------------------
    fo.write("$ Generated by ICEMCFD -  NASTRAN Interface Vers.  4.6.1 \n")
    fo.write("$ Nastran input deck \n")
    fo.write("SOL 103 \n")
    #fo.write("\n")
    
    fo.write("CEND \n")
    #fo.write("\n")
    fo.write("$\n")
    fo.write("BEGIN BULK \n")
        
    #write shell element data
    #------------writing element property data------
    for i in range(0, no_of_shell_elements_new):
        
        fo.write("$CDSCRPT");
        fo.write(str_form('        '));
        fo.write(str_form('        '));
        fo.write(int_form(shell_element_list_new[i].pid));
        fo.write(str_form('        '));
        fo.write(str_form(shell_element_list_new[i].name));
        fo.write("\n");


    fo.write("$\n")
    fo.write("$       grid data              0  \n")


    #------------16 point string----------------

    for i in range(0,no_of_points):
        
        fo.write(str_form('GRID*'));
        fo.write(int_forms(pointlist[i].id));
        fo.write(int_forms(pointlist[i].cp));
        fo.write(float_forms(pointlist[i].x[0]));
        fo.write(float_forms(pointlist[i].x[1]));
        fo.write(str_form('*G'+str(pointlist[i].id)))
        fo.write("\n");
        fo.write(str_form('*G'+str(pointlist[i].id)))
        fo.write(float_forms(pointlist[i].x[2]));
        fo.write(str_form('        '));
        fo.write(int_forms(pointlist[i].cd));
        
        #    fo.write(int_form(pointlist[i].ps));
        #    fo.write(int_form(pointlist[i].seid));
        fo.write("\n");


    #------------writing element data------
    #fo.write("$write element data\n")
    
    #--write to the grid points-

    for i in range(0,no_of_elements):
        
        fo.write(str_form(elemlist[i].type));
        fo.write(int_form(elemlist[i].eid));
        fo.write(int_form(int(element_map[elemlist[i].pid-1])));
        fo.write(int_form(elemlist[i].g[0]));
        fo.write(int_form(elemlist[i].g[1]));
        fo.write(int_form(elemlist[i].g[2]));
        
        if(elemlist[i].type=='CQUAD4'):
            fo.write(int_form(elemlist[i].g[3]));
    
    
        #        fo.write(int_form(global_to_loc_points[elemlist[i].g[0]]));
        #        fo.write(int_form(global_to_loc_points[elemlist[i].g[1]]));
        #        fo.write(int_form(global_to_loc_points[elemlist[i].g[2]]));
        
        #print elemlist[i].g[0],elemlist[i].g[1],elemlist[i].g[2]
        #print global_to_loc_points[elemlist[i].g[0]],elemlist[i].g[1],elemlist[i].g[2]
        
        
        fo.write("\n")



        #-----------------spc data------------
        #fo.write("$spc data\n")
    for i in range(0,no_of_constrained_grid_points):
        #        fo.write(str_form(constrained_grid_point_list[i].type));
        #        fo.write(int_form(constrained_grid_point_list[i].sid));
        #        #fo.write(int_form(constrained_grid_point_list[i].g[0]));
        #
        #        fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
        #        fo.write(int_form(constrained_grid_point_list[i].c1));
        #        fo.write(float_form(constrained_grid_point_list[i].d1));
        
        fo.write(str_form("SPC"));
        #fo.write(str_form('        '));
        #fo.write(format('         '));
        #fo.write(str_form(constrained_grid_point_list[i].type));
        fo.write(int_form(constrained_grid_point_list[i].sid));
        fo.write(int_form(constrained_grid_point_list[i].g1))
        fo.write(int_form(constrained_grid_point_list[i].c1));
        fo.write(float_form(0.0));
        
        #fo.write(float_form(constrained_grid_point_list[i].d1));
        
        
        fo.write("\n");

    fo.write("END BULK")


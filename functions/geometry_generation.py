import numpy as np

import pyFSI

from pyFSI.geomach_aircraft_models.conventional5 import Conventional5
from pyFSI.geomach_aircraft_models.trussbraced_full_str import Trussbraced_full_str
from pyFSI.geomach_aircraft_models.strutbraced import Strutbraced
from pyFSI.geomach_aircraft_models.CRM_wing import CRM_wing

def geometry_generation(aircraft,geomach_structural_mesh,structural_surface_grid_points_file,stl_mesh_filename):

    print "Generating geometry"
    if(aircraft.type=='Conventional'):
        pgm = Conventional5()
        bse = pgm.initialize()
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
        pgm.comps['ltail'].set_airfoil()
        pgm.dvs['lwing_root_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.
        pgm.dvs['lwing_root_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[1] #-1.
        pgm.dvs['lwing_root_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[2] #2.6
        
        #relative to the root
        pgm.dvs['lwing_tip_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[0]-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_tip_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[1]-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_tip_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[2]-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
        
        pgm.dvs['lwing_root_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_chord # 10.0
        pgm.dvs['lwing_mid_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].root_chord # 4.5
        pgm.dvs['lwing_tip_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_chord # 1.2
        
        
        #horz tail
        
        pgm.dvs['ltail_root_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[0] #44.0
        pgm.dvs['ltail_root_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[1] #0.
        pgm.dvs['ltail_root_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[2] #1.3
        
        pgm.dvs['ltail_tip_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[0]-aircraft.main_wing[1].main_wing_section[0].root_origin[0] #6.0
        pgm.dvs['ltail_tip_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[1]-aircraft.main_wing[1].main_wing_section[0].root_origin[1] #1.4
        pgm.dvs['ltail_tip_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[2]-aircraft.main_wing[1].main_wing_section[0].root_origin[2] #8.0
        
        pgm.dvs['ltail_root_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_chord #4.
        #pgm.dvs['ltail_mid_chord'].data[0] = 4.5
        pgm.dvs['ltail_tip_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_chord #1.
        
        
        #vertical tail
        
        
        pgm.dvs['vtail_root_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[0] #42.
        pgm.dvs['vtail_root_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[1] #1.7
        pgm.dvs['vtail_root_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.0
        
        pgm.dvs['vtail_tip_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[0]-aircraft.main_wing[2].main_wing_section[0].root_origin[0] #6.
        pgm.dvs['vtail_tip_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[1]-aircraft.main_wing[2].main_wing_section[0].root_origin[1] #8.
        pgm.dvs['vtail_tip_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[2]-aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.
        
        pgm.dvs['vtail_root_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_chord #5.8
        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
        pgm.dvs['vtail_tip_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_chord #2.0
        
        
        #fuselage
        
        pgm.dvs['fus_root_x'].data[0] = aircraft.fuselage[0].root_origin[0]  #0.
        pgm.dvs['fus_root_y'].data[0] = aircraft.fuselage[0].root_origin[1]  #0.
        pgm.dvs['fus_root_z'].data[0] = aircraft.fuselage[0].root_origin[2]  #0.
        
        pgm.dvs['fus_tip_x'].data[0] = aircraft.fuselage[0].tip_origin[0]  #50.
        pgm.dvs['fus_tip_y'].data[0] = aircraft.fuselage[0].tip_origin[1]  #0.
        pgm.dvs['fus_tip_z'].data[0] = aircraft.fuselage[0].tip_origin[2]  #0.
        
        pgm.dvs['diameter'].data[0] = aircraft.fuselage[0].diameter  #2.6

        pgm.compute_all()

        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()



    if(aircraft.type=='Strut_braced'):
        
        #based on the strut location decide which aircraft 'Strutbraced' should be chosen
        if (aircraft.main_wing[0].strut_section == 1):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_1.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 2):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_2.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 3):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_3.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 4):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_4.Strutbraced()
            #based on the strut location decide which aircraft 'Strutbraced' should be chosen
        elif (aircraft.main_wing[0].strut_section == 5):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_5.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 6):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_6.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 7):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_7.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 8):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_8.Strutbraced()     
        elif (aircraft.main_wing[0].strut_section == 9):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_9.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 10):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_10.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 11):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_11.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 12):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_12.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 13):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_13.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 14):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_14.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 15):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_15.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 16):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_16.Strutbraced()  
        elif (aircraft.main_wing[0].strut_section == 17):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_17.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 18):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_18.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 19):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_19.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 20):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_20.Strutbraced()  
        elif (aircraft.main_wing[0].strut_section == 101):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_101.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 102):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_102.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 103):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_103.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 104):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_104.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 105):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_105.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 106):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_106.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 107):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_107.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 108):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_108.Strutbraced()     
        elif (aircraft.main_wing[0].strut_section == 109):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_109.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 100):
            pgm = pyFSI.geomach_aircraft_models.strut_braced.strutbraced_sectioned_100.Strutbraced()            
        else:
            pgm = Strutbraced()
        
                    #based on the strut location decide which aircraft 'Strutbraced' should be chosen
        
        
        #pgm = Strutbraced()
        #pgm = Trussbraced_full_str()
        bse = pgm.initialize()
        
        
        
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
        pgm.comps['ltail'].set_airfoil('naca0012')
        pgm.comps['vtail'].set_airfoil('naca0010')
        #pgm.dvs['shape_wing_upp'].data[2,2] = 0.0
        
        
        pgm.dvs['lwing_root_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.
        pgm.dvs['lwing_root_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[1] #-1.
        pgm.dvs['lwing_root_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[2] #2.6
        
        #relative to the root
        pgm.dvs['lwing_mid_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].mid_origin[0]-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_mid_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].mid_origin[1]-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_mid_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].mid_origin[2]-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
        
        
        #relative to the root
        pgm.dvs['lwing_tip_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[0]-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_tip_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[1]-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_tip_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[2]-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
        
        pgm.dvs['lwing_root_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_chord # 10.0
        #pgm.dvs['lwing_mid_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].root_chord # 4.5
        pgm.dvs['lwing_tip_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_chord # 1.2
        
        
        #horz tail
        
        pgm.dvs['ltail_root_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[0] #44.0
        pgm.dvs['ltail_root_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[1] #0.
        pgm.dvs['ltail_root_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[2] #1.3
        
        pgm.dvs['ltail_tip_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[0]-aircraft.main_wing[1].main_wing_section[0].root_origin[0] #6.0
        pgm.dvs['ltail_tip_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[1]-aircraft.main_wing[1].main_wing_section[0].root_origin[1] #1.4
        pgm.dvs['ltail_tip_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[2]-aircraft.main_wing[1].main_wing_section[0].root_origin[2] #8.0
        
        pgm.dvs['ltail_root_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_chord #4.
        #pgm.dvs['ltail_mid_chord'].data[0] = 4.5
        pgm.dvs['ltail_tip_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_chord #1.
        
        
        #vertical tail
        
        
        pgm.dvs['vtail_root_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[0] #42.
        pgm.dvs['vtail_root_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[1] #1.7
        pgm.dvs['vtail_root_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.0
        
        pgm.dvs['vtail_tip_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[0]-aircraft.main_wing[2].main_wing_section[0].root_origin[0] #6.
        pgm.dvs['vtail_tip_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[1]-aircraft.main_wing[2].main_wing_section[0].root_origin[1] #8.
        pgm.dvs['vtail_tip_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[2]-aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.
        
        pgm.dvs['vtail_root_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_chord #5.8
        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
        pgm.dvs['vtail_tip_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_chord #2.0
        
        
        #fuselage
        
        pgm.dvs['fus_root_x'].data[0] = aircraft.fuselage[0].root_origin[0]  #0.
        pgm.dvs['fus_root_y'].data[0] = aircraft.fuselage[0].root_origin[1]  #0.
        pgm.dvs['fus_root_z'].data[0] = aircraft.fuselage[0].root_origin[2]  #0.
        
        pgm.dvs['fus_tip_x'].data[0] = aircraft.fuselage[0].tip_origin[0]  #50.
        pgm.dvs['fus_tip_y'].data[0] = aircraft.fuselage[0].tip_origin[1]  #0.
        pgm.dvs['fus_tip_z'].data[0] = aircraft.fuselage[0].tip_origin[2]  #0.
        
        #pgm.dvs['diameter'].data[0] = aircraft.fuselage[0].diameter  #2.6
        
        
        #l-strut
        
        pgm.dvs['lstrut_root_x'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_origin[0] #13.4
        pgm.dvs['lstrut_root_y'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_origin[1] #-1.6
        pgm.dvs['lstrut_root_z'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_origin[2] #2.6
        
        pgm.dvs['lstrut_tip_x'].data[0] = aircraft.main_wing[3].main_wing_section[0].tip_origin[0] - aircraft.main_wing[3].main_wing_section[0].root_origin[0] #1.6
        pgm.dvs['lstrut_tip_y'].data[0] = aircraft.main_wing[3].main_wing_section[0].tip_origin[1] - aircraft.main_wing[3].main_wing_section[0].root_origin[1] #2.6
        pgm.dvs['lstrut_tip_z'].data[0] = aircraft.main_wing[3].main_wing_section[0].tip_origin[2] - aircraft.main_wing[3].main_wing_section[0].root_origin[2] #11.8
        
        pgm.dvs['lstrut_root_chord'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_chord # 1.8
        #pgm.dvs['ltail_mid_chord'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_chord #4.5
        pgm.dvs['lstrut_tip_chord'].data[0] = aircraft.main_wing[3].main_wing_section[0].tip_chord #1.6
        
        
#        #lv
#        
#        pgm.dvs['lv_root_x'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_origin[0] #14.3
#        pgm.dvs['lv_root_y'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_origin[1] #-0.12
#        pgm.dvs['lv_root_z'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_origin[2] #8.8
#        
#        pgm.dvs['lv_tip_x'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_origin[0] - aircraft.main_wing[4].main_wing_section[0].root_origin[0] #0.0
#        pgm.dvs['lv_tip_y'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_origin[1] - aircraft.main_wing[4].main_wing_section[0].root_origin[1] #1.58
#        pgm.dvs['lv_tip_z'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_origin[2] - aircraft.main_wing[4].main_wing_section[0].root_origin[2] #0.0
#        
#        pgm.dvs['lv_root_chord'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_chord #1.1
#        #pgm.dvs['ltail_mid_chord'] = aircraft.main_wing[4].main_wing_section[0].mid_chord #4.5
#        pgm.dvs['lv_tip_chord'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_chord # 1.1

        
        
        
#        #-----prints---------
#        print "lwing_root_x : ",pgm.dvs['lwing_root_x'].data[0]
#        print "lwing_root_y : ",pgm.dvs['lwing_root_y'].data[0]
#        print "lwing_root_z : ",pgm.dvs['lwing_root_z'].data[0]
#        
#        #relative to the root
#        print "lwing_tip_x : ",pgm.dvs['lwing_tip_x'].data[0]
#        print "lwing_tip_y : ",pgm.dvs['lwing_tip_y'].data[0]
#        print "lwing_tip_z : ",pgm.dvs['lwing_tip_z'].data[0]
#        
#        print "lwing_root_chord : ",pgm.dvs['lwing_root_chord'].data[0]
#        #pgm.dvs['lwing_mid_chord'].data[0]
#        print "lwing_tip_chord : ",pgm.dvs['lwing_tip_chord'].data[0]
#        
#        
#        #horz tail
#        
#        print "ltail_root_x : ",pgm.dvs['ltail_root_x'].data[0]
#        print "ltail_root_y : ",pgm.dvs['ltail_root_y'].data[0]
#        print "ltail_root_z : ",pgm.dvs['ltail_root_z'].data[0]
#        
#        print "ltail_tip_x : ",pgm.dvs['ltail_tip_x'].data[0]
#        print "ltail_tip_y : ",pgm.dvs['ltail_tip_y'].data[0]
#        print "ltail_tip_z : ",pgm.dvs['ltail_tip_z'].data[0]
#        
#        print "ltail_root_chord : ",pgm.dvs['ltail_root_chord'].data[0]
#        #pgm.dvs['ltail_mid_chord'].data[0] = 4.5
#        print "ltail_tip_chord : ",pgm.dvs['ltail_tip_chord'].data[0]
#        
#        
#        #vertical tail
#        
#        
#        print "vtail_root_x : ",pgm.dvs['vtail_root_x'].data[0]
#        print "vtail_root_y : ",pgm.dvs['vtail_root_y'].data[0]
#        print "vtail_root_z : ",pgm.dvs['vtail_root_z'].data[0]
#        
#        print "vtail_tip_x : ",pgm.dvs['vtail_tip_x'].data[0]
#        print "vtail_tip_y : ",pgm.dvs['vtail_tip_y'].data[0]
#        print "vtail_tip_z : ",pgm.dvs['vtail_tip_z'].data[0]
#        
#        print "vtail_root_chord : ",pgm.dvs['vtail_root_chord'].data[0]
#        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
#        print "vtail_tip_chord : ",pgm.dvs['vtail_tip_chord'].data[0]
#        
#        
#        #fuselage
#        
#        print "fus_root_x : ",pgm.dvs['fus_root_x'].data[0]
#        print "fus_root_y : ",pgm.dvs['fus_root_y'].data[0]
#        print "fus_root_z : ",pgm.dvs['fus_root_z'].data[0]
#        
#        print "fus_tip_x : ",pgm.dvs['fus_tip_x'].data[0]
#        print "fus_tip_y : ",pgm.dvs['fus_tip_y'].data[0]
#        print "fus_tip_z : ",pgm.dvs['fus_tip_z'].data[0]
#        
#        #pgm.dvs['diameter'].data[0] = aircraft.fuselage[0].diameter  #2.6
#        
#        
        #l-strut
        
        print "lstrut_root_x : ",pgm.dvs['lstrut_root_x'].data[0]
        print "lstrut_root_y : ",pgm.dvs['lstrut_root_y'].data[0]
        print "lstrut_root_z : ",pgm.dvs['lstrut_root_z'].data[0]
        
        print "lstrut_tip_x : ",pgm.dvs['lstrut_tip_x'].data[0]
        print "lstrut_tip_y : ",pgm.dvs['lstrut_tip_y'].data[0]
        print "lstrut_tip_z : ",pgm.dvs['lstrut_tip_z'].data[0]
        
        print "lstrut_root_chord : ",pgm.dvs['lstrut_root_chord'].data[0]
        #pgm.dvs['ltail_mid_chord'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_chord #4.5
        print "lstrut_tip_chord : ",pgm.dvs['lstrut_tip_chord'].data[0]
        
        
        #lv
        
#        print "lv_root_x : ",pgm.dvs['lv_root_x'].data[0]
#        print "lv_root_y : ",pgm.dvs['lv_root_y'].data[0]
#        print "lv_root_z : ",pgm.dvs['lv_root_z'].data[0]
#        
#        print "lv_tip_x : ",pgm.dvs['lv_tip_x'].data[0]
#        print "lv_tip_y : ",pgm.dvs['lv_tip_y'].data[0]
#        print "lv_tip_z : ",pgm.dvs['lv_tip_z'].data[0]
#        
#        print "lv_root_chord : ",pgm.dvs['lv_root_chord'].data[0]
#        #pgm.dvs['ltail_mid_chord'] = aircraft.main_wing[4].main_wing_section[0].mid_chord #4.5
#        print "lv_tip_chord : ",pgm.dvs['lv_tip_chord'].data[0]

        
        

        pgm.compute_all()
        


        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)

        pgm.meshStructure()





    if(aircraft.type=='Strut_braced2'):
        
        #based on the strut location decide which aircraft 'Strutbraced' should be chosen
        if (aircraft.main_wing[0].strut_section == 1):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_1.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 2):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_2.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 3):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_3.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 4):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2strutbraced_sectioned_4.Strutbraced()
            #based on the strut location decide which aircraft 'Strutbraced' should be chosen
        elif (aircraft.main_wing[0].strut_section == 5):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_5.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 6):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_6.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 7):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_7.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 8):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_8.Strutbraced()     
        elif (aircraft.main_wing[0].strut_section == 9):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_9.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 10):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_10.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 11):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_11.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 12):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_12.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 13):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_13.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 14):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_14.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 15):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_15.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 16):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_16.Strutbraced()  
        elif (aircraft.main_wing[0].strut_section == 17):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_17.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 18):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_18.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 19):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_19.Strutbraced()
        elif (aircraft.main_wing[0].strut_section == 20):
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced_sectioned_20.Strutbraced()             
        else:
            pgm = pyFSI.geomach_aircraft_models.strut_braced2.strutbraced.Strutbraced() 
        
        
        
        
        #pgm = Strutbraced()
        #pgm = Trussbraced_full_str()
        bse = pgm.initialize()
        
        
        
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
#        pgm.comps['ltail'].set_airfoil('naca0012')
#        pgm.comps['vtail'].set_airfoil('naca0010')
        #pgm.dvs['shape_wing_upp'].data[2,2] = 0.0
        
        
        pgm.dvs['lwing_root_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.
        pgm.dvs['lwing_root_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[1] #-1.
        pgm.dvs['lwing_root_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[2] #2.6
        
        #relative to the root
        pgm.dvs['lwing_mid_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].mid_origin[0]-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_mid_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].mid_origin[1]-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_mid_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].mid_origin[2]-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
        
        
        #relative to the root
        pgm.dvs['lwing_tip_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[0]-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_tip_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[1]-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_tip_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[2]-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
        
        pgm.dvs['lwing_root_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_chord # 10.0
        #pgm.dvs['lwing_mid_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].root_chord # 4.5
        pgm.dvs['lwing_tip_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_chord # 1.2
        
        
#        #horz tail
#        
#        pgm.dvs['ltail_root_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[0] #44.0
#        pgm.dvs['ltail_root_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[1] #0.
#        pgm.dvs['ltail_root_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[2] #1.3
#        
#        pgm.dvs['ltail_tip_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[0]-aircraft.main_wing[1].main_wing_section[0].root_origin[0] #6.0
#        pgm.dvs['ltail_tip_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[1]-aircraft.main_wing[1].main_wing_section[0].root_origin[1] #1.4
#        pgm.dvs['ltail_tip_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[2]-aircraft.main_wing[1].main_wing_section[0].root_origin[2] #8.0
#        
#        pgm.dvs['ltail_root_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_chord #4.
#        #pgm.dvs['ltail_mid_chord'].data[0] = 4.5
#        pgm.dvs['ltail_tip_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_chord #1.
#        
#        
#        #vertical tail
#        
#        
#        pgm.dvs['vtail_root_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[0] #42.
#        pgm.dvs['vtail_root_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[1] #1.7
#        pgm.dvs['vtail_root_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.0
#        
#        pgm.dvs['vtail_tip_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[0]-aircraft.main_wing[2].main_wing_section[0].root_origin[0] #6.
#        pgm.dvs['vtail_tip_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[1]-aircraft.main_wing[2].main_wing_section[0].root_origin[1] #8.
#        pgm.dvs['vtail_tip_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[2]-aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.
#        
#        pgm.dvs['vtail_root_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_chord #5.8
#        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
#        pgm.dvs['vtail_tip_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_chord #2.0

        
        #fuselage
        
        pgm.dvs['fus_root_x'].data[0] = aircraft.fuselage[0].root_origin[0]  #0.
        pgm.dvs['fus_root_y'].data[0] = aircraft.fuselage[0].root_origin[1]  #0.
        pgm.dvs['fus_root_z'].data[0] = aircraft.fuselage[0].root_origin[2]  #0.
        
        pgm.dvs['fus_tip_x'].data[0] = aircraft.fuselage[0].tip_origin[0]  #50.
        pgm.dvs['fus_tip_y'].data[0] = aircraft.fuselage[0].tip_origin[1]  #0.
        pgm.dvs['fus_tip_z'].data[0] = aircraft.fuselage[0].tip_origin[2]  #0.
        
        #pgm.dvs['diameter'].data[0] = aircraft.fuselage[0].diameter  #2.6
        
        
        #l-strut
        
        pgm.dvs['lstrut_root_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[0] #13.4
        pgm.dvs['lstrut_root_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[1] #-1.6
        pgm.dvs['lstrut_root_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[2] #2.6
        
        pgm.dvs['lstrut_tip_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[0] - aircraft.main_wing[1].main_wing_section[0].root_origin[0] #1.6
        pgm.dvs['lstrut_tip_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[1] - aircraft.main_wing[1].main_wing_section[0].root_origin[1] #2.6
        pgm.dvs['lstrut_tip_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[2] - aircraft.main_wing[1].main_wing_section[0].root_origin[2] #11.8
        
        pgm.dvs['lstrut_root_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_chord # 1.8
        #pgm.dvs['ltail_mid_chord'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_chord #4.5
        pgm.dvs['lstrut_tip_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_chord #1.6
        
        
#        #lv
#        
#        pgm.dvs['lv_root_x'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_origin[0] #14.3
#        pgm.dvs['lv_root_y'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_origin[1] #-0.12
#        pgm.dvs['lv_root_z'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_origin[2] #8.8
#        
#        pgm.dvs['lv_tip_x'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_origin[0] - aircraft.main_wing[4].main_wing_section[0].root_origin[0] #0.0
#        pgm.dvs['lv_tip_y'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_origin[1] - aircraft.main_wing[4].main_wing_section[0].root_origin[1] #1.58
#        pgm.dvs['lv_tip_z'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_origin[2] - aircraft.main_wing[4].main_wing_section[0].root_origin[2] #0.0
#        
#        pgm.dvs['lv_root_chord'].data[0] = aircraft.main_wing[4].main_wing_section[0].root_chord #1.1
#        #pgm.dvs['ltail_mid_chord'] = aircraft.main_wing[4].main_wing_section[0].mid_chord #4.5
#        pgm.dvs['lv_tip_chord'].data[0] = aircraft.main_wing[4].main_wing_section[0].tip_chord # 1.1

        
        
        
#        #-----prints---------
#        print "lwing_root_x : ",pgm.dvs['lwing_root_x'].data[0]
#        print "lwing_root_y : ",pgm.dvs['lwing_root_y'].data[0]
#        print "lwing_root_z : ",pgm.dvs['lwing_root_z'].data[0]
#        
#        #relative to the root
#        print "lwing_tip_x : ",pgm.dvs['lwing_tip_x'].data[0]
#        print "lwing_tip_y : ",pgm.dvs['lwing_tip_y'].data[0]
#        print "lwing_tip_z : ",pgm.dvs['lwing_tip_z'].data[0]
#        
#        print "lwing_root_chord : ",pgm.dvs['lwing_root_chord'].data[0]
#        #pgm.dvs['lwing_mid_chord'].data[0]
#        print "lwing_tip_chord : ",pgm.dvs['lwing_tip_chord'].data[0]
#        
#        
#        #horz tail
#        
#        print "ltail_root_x : ",pgm.dvs['ltail_root_x'].data[0]
#        print "ltail_root_y : ",pgm.dvs['ltail_root_y'].data[0]
#        print "ltail_root_z : ",pgm.dvs['ltail_root_z'].data[0]
#        
#        print "ltail_tip_x : ",pgm.dvs['ltail_tip_x'].data[0]
#        print "ltail_tip_y : ",pgm.dvs['ltail_tip_y'].data[0]
#        print "ltail_tip_z : ",pgm.dvs['ltail_tip_z'].data[0]
#        
#        print "ltail_root_chord : ",pgm.dvs['ltail_root_chord'].data[0]
#        #pgm.dvs['ltail_mid_chord'].data[0] = 4.5
#        print "ltail_tip_chord : ",pgm.dvs['ltail_tip_chord'].data[0]
#        
#        
#        #vertical tail
#        
#        
#        print "vtail_root_x : ",pgm.dvs['vtail_root_x'].data[0]
#        print "vtail_root_y : ",pgm.dvs['vtail_root_y'].data[0]
#        print "vtail_root_z : ",pgm.dvs['vtail_root_z'].data[0]
#        
#        print "vtail_tip_x : ",pgm.dvs['vtail_tip_x'].data[0]
#        print "vtail_tip_y : ",pgm.dvs['vtail_tip_y'].data[0]
#        print "vtail_tip_z : ",pgm.dvs['vtail_tip_z'].data[0]
#        
#        print "vtail_root_chord : ",pgm.dvs['vtail_root_chord'].data[0]
#        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
#        print "vtail_tip_chord : ",pgm.dvs['vtail_tip_chord'].data[0]
#        
#        
#        #fuselage
#        
#        print "fus_root_x : ",pgm.dvs['fus_root_x'].data[0]
#        print "fus_root_y : ",pgm.dvs['fus_root_y'].data[0]
#        print "fus_root_z : ",pgm.dvs['fus_root_z'].data[0]
#        
#        print "fus_tip_x : ",pgm.dvs['fus_tip_x'].data[0]
#        print "fus_tip_y : ",pgm.dvs['fus_tip_y'].data[0]
#        print "fus_tip_z : ",pgm.dvs['fus_tip_z'].data[0]
#        
#        #pgm.dvs['diameter'].data[0] = aircraft.fuselage[0].diameter  #2.6
#        
#        
        #l-strut
        
        print "lstrut_root_x : ",pgm.dvs['lstrut_root_x'].data[0]
        print "lstrut_root_y : ",pgm.dvs['lstrut_root_y'].data[0]
        print "lstrut_root_z : ",pgm.dvs['lstrut_root_z'].data[0]
        
        print "lstrut_tip_x : ",pgm.dvs['lstrut_tip_x'].data[0]
        print "lstrut_tip_y : ",pgm.dvs['lstrut_tip_y'].data[0]
        print "lstrut_tip_z : ",pgm.dvs['lstrut_tip_z'].data[0]
        
        print "lstrut_root_chord : ",pgm.dvs['lstrut_root_chord'].data[0]
        #pgm.dvs['ltail_mid_chord'].data[0] = aircraft.main_wing[3].main_wing_section[0].root_chord #4.5
        print "lstrut_tip_chord : ",pgm.dvs['lstrut_tip_chord'].data[0]
        
        
        #lv
        
#        print "lv_root_x : ",pgm.dvs['lv_root_x'].data[0]
#        print "lv_root_y : ",pgm.dvs['lv_root_y'].data[0]
#        print "lv_root_z : ",pgm.dvs['lv_root_z'].data[0]
#        
#        print "lv_tip_x : ",pgm.dvs['lv_tip_x'].data[0]
#        print "lv_tip_y : ",pgm.dvs['lv_tip_y'].data[0]
#        print "lv_tip_z : ",pgm.dvs['lv_tip_z'].data[0]
#        
#        print "lv_root_chord : ",pgm.dvs['lv_root_chord'].data[0]
#        #pgm.dvs['ltail_mid_chord'] = aircraft.main_wing[4].main_wing_section[0].mid_chord #4.5
#        print "lv_tip_chord : ",pgm.dvs['lv_tip_chord'].data[0]

        
        

        pgm.compute_all()
        


        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)

        pgm.meshStructure()





    print "Generating geometry"
    if(aircraft.type=='CRM_wing'):
        pgm = CRM_wing()
        bse = pgm.initialize()
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
        pgm.dvs['lwing_root_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.
        pgm.dvs['lwing_root_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[1] #-1.
        pgm.dvs['lwing_root_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[2] #2.6
        
        #relative to the root
        pgm.dvs['lwing_tip_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[0]-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_tip_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[1]-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_tip_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[2]-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
        
        pgm.dvs['lwing_root_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_chord # 10.0
        pgm.dvs['lwing_mid_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].root_chord # 4.5
        pgm.dvs['lwing_tip_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_chord # 1.2
        
        pgm.compute_all()
        
        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()

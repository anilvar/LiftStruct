import numpy as np

from pyFSI.geomach_aircraft_models.conventional5 import Conventional5
from pyFSI.geomach_aircraft_models.trussbraced_full_str import Trussbraced_full_str

def geometry_generation(aircraft,geomach_structural_mesh,structural_surface_grid_points_file,stl_mesh_filename):

    print "Generating geometry"
    if(aircraft.type=='Conventional'):
        pgm = Conventional5()
        bse = pgm.initialize()
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
        pgm.comps['ltail'].set_airfoil()
        pgm.dvs['shape_wing_upp'].data[2,2] = 0.0
        pgm.dvs['span'].data[0] = aircraft.main_wing.span
        pgm.dvs['root_chord'].data[0] = aircraft.main_wing.main_wing_section[0].root_chord
        pgm.dvs['mid_chord'].data[0] = 4.5 #aircraft.main_wing.main_wing_section[0].tip_chord
        pgm.dvs['tip_chord'].data[0] = aircraft.main_wing.tip_chord
        pgm.dvs['tip_chord_z'].data[0] = aircraft.main_wing.tip_origin[0] - aircraft.main_wing.root_origin[0]
        pgm.dvs['wing_z_pos'].data[0] = aircraft.fuselage.diameter
        pgm.dvs['wing_x_pos'].data[0] = aircraft.main_wing.root_origin[0]
        #
        pgm.dvs['fuselage_length'].data[0] = aircraft.fuselage.length
        pgm.dvs['diameter'].data[0] = aircraft.fuselage.diameter
        pgm.compute_all()
        

#	print pgm.dvs['span'].data[0] 
#        print pgm.dvs['root_chord'].data[0] 
#        print pgm.dvs['mid_chord'].data[0] 
#        print pgm.dvs['tip_chord'].data[0] 
#        print pgm.dvs['tip_chord_z'].data[0] 
#        print pgm.dvs['wing_z_pos'].data[0] 
#        print pgm.dvs['wing_x_pos'].data[0] 
#        #
#        print pgm.dvs['fuselage_length'].data[0] 
#        print pgm.dvs['diameter'].data[0] 


        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()



    if(aircraft.type=='Strut_braced'):
        pgm = Trussbraced_full_str()
        bse = pgm.initialize()
        
        
        
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
        pgm.comps['ltail'].set_airfoil('naca0012')
        pgm.comps['vtail'].set_airfoil('naca0010')
        #pgm.dvs['shape_wing_upp'].data[2,2] = 0.0
        pgm.dvs['span'].data[0] = aircraft.main_wing.span
        pgm.dvs['root_chord'].data[0] = aircraft.main_wing.main_wing_section[0].root_chord
        #pgm.dvs['mid_chord'].data[0] = aircraft.main_wing.main_wing_section[0].tip_chord
        pgm.dvs['tip_chord'].data[0] = aircraft.main_wing.tip_chord
        pgm.dvs['tip_chord_z'].data[0] = aircraft.main_wing.tip_origin[0] - aircraft.main_wing.root_origin[0]
        pgm.dvs['wing_z_pos'].data[0] = aircraft.fuselage.diameter
        pgm.dvs['wing_x_pos'].data[0] = aircraft.main_wing.root_origin[0]
        #
        pgm.dvs['fuselage_length'].data[0] = aircraft.fuselage.length
        #pgm.dvs['diameter'].data[0] = aircraft.fuselage.diameter
        pgm.dvs['strut_z_position'].data[0] = aircraft.main_wing.strut_location[2]
        pgm.compute_all()
        
        print pgm.dvs['span'].data[0]
        print pgm.dvs['root_chord'].data[0]
        print pgm.dvs['tip_chord'].data[0]
        print pgm.dvs['tip_chord_z'].data[0]
        print pgm.dvs['wing_z_pos'].data[0]
        print pgm.dvs['wing_x_pos'].data[0]
        #
        print pgm.dvs['fuselage_length'].data[0]
        print pgm.dvs['strut_z_position'].data[0]

        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()

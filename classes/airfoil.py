#---Class structure for this----------------------
from pyFSI.class_str.grid.class_structure import grid
from pyFSI.input.read_geomach_surface_points import read_geomach_surface_points
from pyFSI.input.read_stl_meshfile import read_stl_meshfile
from pyFSI.functions.compute_aircraft_loads import compute_aerodynamic_loads
from structural_dvs import structural_dvs
from mpl_toolkits.mplot3d import Axes3D

from scipy.interpolate import interp1d

import numpy as np
import matplotlib.pyplot as plt

class airfoil:
    
    def __init__(self):
    
        self.type =  'airfoil'
        self.pointlist_upper = []
        self.pointlist_lower = []
        self.cp_upper = []
        self.cp_lower = []
    



    def read_airfoil_file(self,airfoil_name):
        #get the cp_upper and the cp_lower as well as the pointlist_upper and pointlist_lower
        mesh_filename_upper = airfoil_name + "_u"+ ".csv"
        mesh_filename_lower = airfoil_name + "_l"+ ".csv"
        
        
        #upper surface
        file = open(mesh_filename_upper, 'r')
    
        no_of_upper_points = 0
        for line in file:
            no_of_upper_points += 1


        file.close()
            


        self.pointlist_upper = np.array(no_of_upper_points)
        self.cp_upper = np.array(no_of_upper_points)
        file = open(mesh_filename_upper, 'r')
    
        no_of_upper_points = 0
        for line in file:
            line_val = line.split(",")
            self.pointlist_upper[no_of_upper_points] = float(line_val[0])
            self.cp_upper[no_of_upper_points] = float(line_val[1])
            no_of_upper_points += 1


        file.close()



        #lower surface
        file = open(mesh_filename_upper, 'r')
    
        no_of_lower_points = 0
        for line in file:
            no_of_lower_points += 1


        file.close()
        
        self.pointlist_lower = np.array(no_of_lower_points)
        self.cp_lower = np.array(no_of_lower_points)
        file = open(mesh_filename_upper, 'r')
        
        no_of_lower_points = 0
        for line in file:
            line_val = line.split(",")
            self.pointlist_lower[no_of_lower_points] = float(line_val[0])
            self.cp_lower[no_of_lower_points] = float(line_val[1])
            no_of_lower_points += 1
        
        
        file.close()





    def interpolate_loads(self):
        cp_upper_interp = interp1d(self.pointlist_upper, self.cp_upper, kind='cubic')
        cp_lower_interp = interp1d(self.pointlist_lower, self.cp_lower, kind='cubic')
    
        self.cp_upper_interp = cp_upper_interp
        self.cp_lower_interp = cp_lower_interp
    

    #location is the chordwise location, position is upper or lower surface
    def compute_load(self,chord,location,position,pfreestream):

        non_dimensional_position = location/chord
        local_cp = 0.0
        local_pressure = 0.0

        if (position == "upper"):
            local_cp = self.cp_upper_interp(non_dimensional_position)

        elif (position == "lower"):
            local_cp = self.cp_lower_interp(non_dimensional_position)


        local_pressure = local_cp*pfreestream

        return local_pressure



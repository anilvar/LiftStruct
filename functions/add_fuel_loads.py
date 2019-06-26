import numpy as np
def add_fuel_loads(aircraft):

#loop over the wings
#check if the contains_fuel tag is active
#pull out the starting and ending  x,y and z of the fule loads
#loop over the wing lower surface
#add the fuel load weight

#need to loop over the structural mesh and look at the wing lower surface elements


#loop over the elements in the wing lower surface (get the point id's)
#split the loads uniformly among the lower surface points



    for wng in range(0,len(aircraft.main_wing)):
        
        if(aircraft.main_wing[wng].contains_fuel == 1):

        
            load = aircraft.main_wing[wng].fuel_load

        
    

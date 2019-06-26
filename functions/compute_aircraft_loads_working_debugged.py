import numpy as np
def compute_aerodynamic_loads(aircraft):

    #Unpack

    for wng in range(0,len(aircraft.main_wing)):
    
        aircraft.main_wing[wng].total_force = 0.0
        aircraft.main_wing[wng].total_area = 0.0
        MTOW = aircraft.MTOW
        span = aircraft.main_wing[wng].span
        no_of_gridelements_chordwise = aircraft.no_of_gridelements_chordwise
    #    no_of_grid_elements_spanwise = aircraft.no_of_grid_elements_spanwise

        half_lift =  aircraft.main_wing[wng].sizing_lift #MTOW/2.0*9.81*2.5  #2.5g
        print "half lift", half_lift
        half_span =  span

        max_lift = 0.5*(2.0*half_lift/half_span)  #the multiplication by 0.5 is for the lift on both sides of the wing
        root_origin_y = aircraft.main_wing[wng].main_wing_section[0].root_origin[1]
        
        compute_total_force = 0.
       
        if(aircraft.main_wing[wng].vertical == 0):

            print "Loading Wing ",wng
            #loop over the points for the main wing

            for i in range(0,len(aircraft.pointlist)):


                element_lift = 0.0
                if(aircraft.pointlist[i].part==("w_"+str(wng))):
                    relative_z = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[0].root_origin[2]


                    current_span = 0.0
                    current_rchord = 0.0
                    current_tchord = 0.0
                    current_z_global = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[0].root_origin[2]
                    for j  in range(0,aircraft.main_wing[wng].no_of_sections):
                        prev_span = current_span
                        current_span = current_span + aircraft.main_wing[wng].main_wing_section[j].span
                        current_rchord = aircraft.main_wing[wng].main_wing_section[j].root_chord
                        current_tchord = aircraft.main_wing[wng].main_wing_section[j].tip_chord

                
                        #print aircraft.pointlist[i].x[2]-aircraft.main_wing.main_wing_section[0].root_origin[2], prev_span, current_span
                        if aircraft.pointlist[i].x[2]-aircraft.main_wing[wng].main_wing_section[0].root_origin[2]>prev_span and aircraft.pointlist[i].x[2]-aircraft.main_wing[wng].main_wing_section[0].root_origin[2]<current_span:
                            current_taper = current_tchord/current_rchord
                            current_z_local = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[j].root_origin[2]
                            
                            si  = current_z_local/aircraft.main_wing[wng].main_wing_section[j].span
                            
                            #current_chord = current_z_local/aircraft.main_wing[wng].main_wing_section[j].span * current_taper
                            current_chord = si*current_tchord + (1-si)*current_rchord 
                            
                            current_leading_edge = aircraft.main_wing[wng].main_wing_section[j].root_origin + current_z_local*np.tan(aircraft.main_wing[wng].main_wing_section[j].sweep)
                            current_x_local = aircraft.pointlist[i].x[0] - current_leading_edge
                            
                            spanwise_lift = (1-current_z_global/half_span)*max_lift #l(y)

                            chordwise_lift = spanwise_lift/current_chord
                            
                            element_lift = chordwise_lift * aircraft.pointlist[i].Sarea
                            
                            aircraft.main_wing[wng].total_force += element_lift
                            aircraft.main_wing[wng].total_area += aircraft.pointlist[i].Sarea
                            
                            #print i,current_z_local,current_chord,spanwise_lift,aircraft.pointlist[i].Sarea
                            
                            if(aircraft.pointlist[i].normal[1]>=0.0):
                            
                                aircraft.pointlist[i].f[0] = 0.0
                                aircraft.pointlist[i].f[1] = element_lift
                                aircraft.pointlist[i].f[2] = 0.0
                                aircraft.pointlist[i].chord = current_chord
                            
                            
                            
                            else:
                            
                                aircraft.pointlist[i].f[0] = 0.0
                                aircraft.pointlist[i].f[1] = element_lift
                                aircraft.pointlist[i].f[2] = 0.0
                                aircraft.pointlist[i].chord = current_chord

                            current_section = j

                            #print aircraft.pointlist[i].Sarea

                            break
                            




        if(aircraft.main_wing[wng].vertical == 0):

            print "Loading Wing ",wng
            #loop over the points for the main wing

            for i in range(0,len(aircraft.pointlist)):


                element_lift = 0.0
                if(aircraft.pointlist[i].part==("w_"+str(wng))):
                    relative_z = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[0].root_origin[2]


                    current_span = 0.0
                    current_rchord = 0.0
                    current_tchord = 0.0
                    current_z_global = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[0].root_origin[2]
                    for j  in range(0,aircraft.main_wing[wng].no_of_sections):
                        prev_span = current_span
                        current_span = current_span + aircraft.main_wing[wng].main_wing_section[j].span
                        current_rchord = aircraft.main_wing[wng].main_wing_section[j].root_chord
                        current_tchord = aircraft.main_wing[wng].main_wing_section[j].tip_chord

                
                        #print aircraft.pointlist[i].x[2]-aircraft.main_wing.main_wing_section[0].root_origin[2], prev_span, current_span
                        if aircraft.pointlist[i].x[2]-aircraft.main_wing[wng].main_wing_section[0].root_origin[2]>prev_span and aircraft.pointlist[i].x[2]-aircraft.main_wing[wng].main_wing_section[0].root_origin[2]<current_span:
                            current_taper = current_tchord/current_rchord
                            current_z_local = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[j].root_origin[2]
                            
                            si  = current_z_local/aircraft.main_wing[wng].main_wing_section[j].span
                            
                            #current_chord = current_z_local/aircraft.main_wing[wng].main_wing_section[j].span * current_taper
                            current_chord = si*current_tchord + (1-si)*current_rchord 
                            
                            current_leading_edge = aircraft.main_wing[wng].main_wing_section[j].root_origin + current_z_local*np.tan(aircraft.main_wing[wng].main_wing_section[j].sweep)
                            current_x_local = aircraft.pointlist[i].x[0] - current_leading_edge
                            
                            spanwise_lift = (1-current_z_global/half_span)*max_lift #l(y)

                            chordwise_lift = spanwise_lift/current_chord
                            
                            element_lift = chordwise_lift * aircraft.pointlist[i].Sarea
                            
                            aircraft.main_wing[wng].total_force += element_lift
                            aircraft.main_wing[wng].total_area += aircraft.pointlist[i].Sarea
                            
                            #print i,current_z_local,current_chord,spanwise_lift,aircraft.pointlist[i].Sarea
                            
                            if(aircraft.pointlist[i].normal[1]>=0.0):
                            
                                aircraft.pointlist[i].f[0] = 0.0
                                aircraft.pointlist[i].f[1] = element_lift
                                aircraft.pointlist[i].f[2] = 0.0
                                aircraft.pointlist[i].chord = current_chord
                            
                            
                            
                            else:
                            
                                aircraft.pointlist[i].f[0] = 0.0
                                aircraft.pointlist[i].f[1] = element_lift
                                aircraft.pointlist[i].f[2] = 0.0
                                aircraft.pointlist[i].chord = current_chord

                            current_section = j

                            #print aircraft.pointlist[i].Sarea

                            break
                            





    for fus in range(0,len(aircraft.fuselage)):
        for i in range(0,len(aircraft.pointlist)):
            if(aircraft.pointlist[i].part=="f_"+str(fus)):
                

                aircraft.pointlist[i].f[0] = aircraft.pointlist[i].normal[0]*aircraft.internal_pressure* aircraft.pointlist[i].Sarea
                aircraft.pointlist[i].f[1] = aircraft.pointlist[i].normal[1]*aircraft.internal_pressure* aircraft.pointlist[i].Sarea
                aircraft.pointlist[i].f[2] = aircraft.pointlist[i].normal[2]*aircraft.internal_pressure* aircraft.pointlist[i].Sarea





#compute the internal pressure loads



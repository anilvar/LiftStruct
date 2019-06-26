#from nearest_point_interpolation import nearest_point_interpolation  #*



def interpolate_loads(pointlist_fl,pointlist_str,elemlist):




    mesh_def = open("loads.txt","wb")

    #write load file
    for i in range(0,len(pointlist_fl)):
        mesh_def.write(format(pointlist_fl[i].x[0]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_fl[i].x[1]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_fl[i].x[2]))
        mesh_def.write("\n")


    for i in range(0,len(pointlist_str)):
        mesh_def.write(format(pointlist_str[i].x[0]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_str[i].x[1]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_str[i].x[2]))
        mesh_def.write("\n")


    mesh_def.close()

    no_of_fluid_points = len(pointlist_fl)
    no_of_structure_points = len(pointlist_str)

    #mampp = nearest_point_interpolation(no_of_fluid_points, no_of_structure_points)


    print "Done with interpolation"

    file = open("interpolation.txt", 'r')

    for i in range(0,len(pointlist_fl)):
        for line in file:
            
            closest_point = int(line);
            pointlist_fl[i].str_point = closest_point + 1;
            pointlist_str[closest_point].pressure=pointlist_str[closest_point].pressure + pointlist_fl[i].pressure

            pointlist_str[closest_point].f[0]=pointlist_str[closest_point].f[0] + pointlist_fl[i].f[0]
            pointlist_str[closest_point].f[1]=pointlist_str[closest_point].f[1] + pointlist_fl[i].f[1]
            pointlist_str[closest_point].f[2]=pointlist_str[closest_point].f[2] + pointlist_fl[i].f[2]
            pointlist_str[closest_point].fl_gridpt=pointlist_fl[i].id
            
            break





#read values from load file
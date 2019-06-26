/*!
compute nearest point
 */

//void nearest_point_interpolation(double **fl, double **str, int no_of_fluid_points, int no_of_structure_points, int *point_map){

#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;


void nearest_point_interpolation(int no_of_fluid_points, int no_of_structure_points){
    
    ifstream mesh_file;
    ofstream output_file;
    char meshfile[200];
    int closest_point;
    double distance;
    double minimum_distance;
    unsigned long point_map[no_of_fluid_points];
    //int *point_map;
    //double fl[no_of_fluid_points][3];
    double ** fl;
    fl =  new double *[no_of_fluid_points];
    for (int i=0;i<no_of_fluid_points;i++){
        
        fl[i]  = new double[3];
        
    }
    
    
    
    //double str[no_of_structure_points][3];
    double ** str;
    str =  new double *[no_of_structure_points];
    for (int i=0;i<no_of_structure_points;i++){
        
        str[i]  = new double[3];
        
    }
    
    
    string text_line;
    
    //read the fluid and structure points from the specified filename
    
    mesh_file.open("loads.txt", ios::in);
    for (int iPoint = 0; iPoint < no_of_fluid_points; iPoint ++) {
        getline(mesh_file, text_line);
        istringstream point_line(text_line);
        point_line >> fl[iPoint][0]; point_line >> fl[iPoint][1];point_line >> fl[iPoint][2];
    }
    
    for (int iPoint = 0; iPoint < no_of_structure_points; iPoint ++) {
        getline(mesh_file, text_line);
        istringstream point_line(text_line);
        point_line >> str[iPoint][0]; point_line >> str[iPoint][1];point_line >> str[iPoint][2];
    }
    
    
     mesh_file.close();
    
    // interpolate the mesh
    for(int i=0;i<no_of_fluid_points;i++){
        
        minimum_distance = (fl[i][0] -str[0][0])*(fl[i][0] -str[0][0]) + (fl[i][1] -str[0][1])*(fl[i][1] -str[0][1]) + (fl[i][2] -str[0][2])*(fl[i][2] -str[0][2]);
        closest_point = 0;
        
        
        for (int j=1;j<no_of_structure_points;j++){
            
            distance = (fl[i][0] -str[j][0])*(fl[i][0] -str[j][0]) + (fl[i][1] -str[j][1])*(fl[i][1] -str[j][1]) + (fl[i][2] -str[j][2])*(fl[i][2] -str[j][2]);
            
            if(distance<minimum_distance){
                minimum_distance = distance;
                closest_point = j;
                
            }
            
        }
        
        point_map[i] = closest_point;
        
        
    }
    

    
    output_file.open("interpolation.txt", ios::out);
    for (int iPoint = 0; iPoint < no_of_fluid_points; iPoint ++) {
        output_file << point_map[iPoint] << "\n";
    }
    
    
    output_file.close();

    
    for (int i=0;i<no_of_fluid_points;i++){
        
         delete[] fl[i];
        
    }
    delete[] fl;
    
    

    for (int i=0;i<no_of_structure_points;i++){
        
         delete[] str[i];
        
    }

    delete[] str;
    
    
    
    
    
    
    
    
    
}



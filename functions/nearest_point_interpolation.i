%module nearest_point_interpolation

%{
    
#define SWIG_FILE_WITH_INIT

#include <stdlib.h>
#include <stdio.h>
#include "nearest_point_interpolation.h"

%}

%include "numpy.i"
%include "std_string.i"
%include "std_map.i"
%include "std_vector.i"
%include "nearest_point_interpolation.h"


    
void nearest_point_interpolation(int no_of_fluid_points, int no_of_structure_points);
    








# script you can run to make g-code for the router - 20240117 CJH
# circles or center drill points
# check your work by pasting to https://ncviewer.com/

import simplegcode as sg
import numpy as np

# CHANGE PARAMETERS IN THIS SECTION - CHOOSE GRID OR PERIMETER
output_file_description = 'test_circles'

# simple way to generate a grid or perimeter - update these as needed
perimeter_only = True  # forces entire grid or just the perimeter
x_start, x_final, x_spacing = 0.5, 2.5, 1.0  # inches
y_start, y_final, y_spacing = 0.5, 4.5, 1.0

# update these as needed for the G-code instructions
mill_circles = True  # false if you only want to drill
depth = -0.26  # depth in Z for the operation (single step in this version)
hole_diameter = (0.205-0.125)  # if you want to mill out a circle, subtract tool diameter manually here
machine = 'shapeoko'  # shapeoko or benchmill, ON BENCHMILL YOU MAY NEED TO ADD A % FOR FANUC MODE
display_plot = False  # show a plot of the points after generating
time_stamp = False  # timestamp the file name
sweeps = 2  # number of inside sweeps of each circle when cutting

# -----------------------  do not modify beLow this line   -----------------------
if perimeter_only:  # simple way to generate a perimeter - or any legs of a perimeter
    point_list = [(x_, y_) for x_ in np.arange(x_start, x_final+x_spacing, x_spacing) for y_ in [y_start]]  # bottom row
    point_list += [(x_, y_) for x_ in [x_final] for y_ in np.arange(y_start+y_spacing, y_final+y_spacing, y_spacing) ]  # right col
    point_list += [(x_, y_) for x_ in np.arange(x_final-x_spacing, x_start-x_spacing, -x_spacing) for y_ in [y_final]]  # top row
    point_list += [(x_, y_) for x_ in [x_start] for y_ in np.arange(y_final-y_spacing, y_start, -y_spacing) ]  # left col
else:  # generate a grid
    x = [x_ for x_ in np.arange(x_start, x_final + x_spacing, x_spacing)]
    y = [y_ for y_ in  np.arange(y_start, y_final + y_spacing, y_spacing)]
    point_list = [(x_, y_) for x_ in x for y_ in y]

# -----------------------  WRITE THE FILE   -----------------------
overrides = {'DRILL_FEED':2,'DRILL_DEPTH':depth, 'RETRACT_HEIGHT': 0.5, 'ENGAGE_HEIGHT': 0.05, "CUT_FEED":8,
            'MILL_CIRCLES':mill_circles, 'HOLE_DIAMETER':hole_diameter, 'SWEEPS': sweeps} # dictionary of what to change from default
code = sg.generate_gcode(point_list, machine=machine, peck=False, overrides=overrides,
                         save_file=True, file_description=output_file_description, time_stamp=time_stamp)

print(f'Probably generated a file looking like {output_file_description}_shapeoko_circles.nc ...')

if display_plot:  # put up a map of your points to double check
    sg.plot_points(point_list, annotate=False, show_order=True, interactive=False)
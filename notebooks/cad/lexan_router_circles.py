# script you can run to make g-code for the router - 20240117 CJH
# circles or center drill points

import simplegcode as sg
import numpy as np

# CHANGE PARAMETERS IN THIS SECTION - CHOOSE GRID OR PERIMETER
output_file_description = 'test'

perimeter_only = True  # will only do perimeter if this is True
x_start, x_spacing = 0.0, 1.0  # negatives are fine
y_start, y_spacing = 0.0, 1
x_repeats = 3  # minimum 1
y_repeats = 3  # minimum 1
mill_circles = True  # false if you only want to drill
depth = -0.26  # depth in Z for the operation (single step in this version)
hole_diameter = (0.200-0.125)  # if you want to mill out a circle
machine = 'shapeoko'  # shapeoko or benchmill
display_plot = False  # show a plot of the points
time_stamp = False  # timestamp the file name
sweeps = 2 # number of sweeps

# -----------------------  do not modify beLow this line   -----------------------
if perimeter_only:  # will be hollow once
    x_final = x_start + x_spacing * (x_repeats-1)  # minimum 1
    y_final = y_start + y_spacing * (y_repeats-1)  # minimum 1
    point_list = [(x_, y_) for x_ in np.arange(x_start, x_final+x_spacing, x_spacing) for y_ in [y_start]]  # bottom row
    point_list += [(x_, y_) for x_ in [x_final] for y_ in np.arange(y_start+y_spacing, y_final+y_spacing, y_spacing) ]  # right col
    point_list += [(x_, y_) for x_ in np.arange(x_final-x_spacing, x_start-x_spacing, -x_spacing) for y_ in [y_final]]  # top row
    point_list += [(x_, y_) for x_ in [x_start] for y_ in np.arange(y_final-y_spacing, y_start, -y_spacing) ]  # left col
else:
    x = [x_start + x_spacing * _ for _ in range(x_repeats)]
    y = [y_start + y_spacing * _ for _ in range(y_repeats)]
    point_list = [(x_, y_) for x_ in x for y_ in y]

# -----------------------  WRITE THE FILE   -----------------------
overrides = {'DRILL_FEED':2,'DRILL_DEPTH':depth, 'RETRACT_HEIGHT': 0.5, 'ENGAGE_HEIGHT': 0.05,
            'MILL_CIRCLES':mill_circles, 'HOLE_DIAMETER':hole_diameter, 'SWEEPS': sweeps} # dictionary of what to change from default
code = sg.generate_gcode(point_list, machine=machine, peck=False, overrides=overrides,
                         save_file=True, file_description=output_file_description, time_stamp=time_stamp)

print(f'Probably generated a file looking like {output_file_description}_shapeoko_circles.nc ...')

if display_plot:
    sg.plot_points(point_list, annotate=False, show_order=True, interactive=False)
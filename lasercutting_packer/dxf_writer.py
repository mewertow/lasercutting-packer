from dxfwrite import DXFEngine as dxf
import numpy as np
import os
import datetime


def generate_dxf(layouts_list):
    """
    Generate dxfs for each layout. Name the file based on the mat spec:
    Date_mat_color_W_H_numpanel
    Save file in directory based on job# (batch#?)
    """

    # Create new directory with job name
    dir_path = create_dir("TEST")

    # For each layout, create a new dir:
    for l in layouts_list:
        color = l.color
        thickness = l.thickness
        file_path = os.path.join(
            dir_path, "{0}_{1}mm".format(l.color, l.thickness))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        os.chdir(file_path)

        # for each panel in the layout
        index = 0
        for panel in l.layout:
            drawing = dxf.drawing('panel_{}_w_{}_h_{}.dxf'.format(
                index, panel.width, panel.height))
            drawing.add_layer('LINES')
            for rect in panel:
                x = rect.x
                y = rect.y
                w = rect.width
                h = rect.height

                drawing.add(dxf.line((x, y), (x + w, y),
                                     color=7, layer='LINES'))
                drawing.add(dxf.line((x + w, y), (x + w, y + h),
                                     color=7, layer='LINES'))
                drawing.add(dxf.line((x + w, y + h),
                                     (x, y + h), color=7, layer='LINES'))
                drawing.add(dxf.line((x, y + h), (x, y),
                                     color=7, layer='LINES'))
            drawing.save()
            index += 1


def create_dir(dirname):
    """creates directory with spec'd name here."""
    current_directory = os.getcwd()
    # date = datetime.datetime()
    timestamp = datetime.date.today()
    folder_name = "{0}_{1}".format(timestamp, dirname)
    dir_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path


# num_bins = len(layout)

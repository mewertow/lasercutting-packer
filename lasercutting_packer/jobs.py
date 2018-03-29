from rectpack import newPacker, float2dec
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from time import sleep


class Job(object):
    """
    A job is intended to be run on one type of material, hence thickness and color and material should be fixed. It contains all the portions from all designs that fit that specification in a list of tuples (width,height)
    """

    def __init__(self, color, thickness, cut_list=[]):
        self.color = color
        self.thickness = thickness
        self.cut_list = cut_list[:]
        self.job_size = len(self.cut_list)

    def update_cut_list(self, new_cuts):
        """Update the cut list for the job"""
        self.cut_list.extend(new_cuts[:])
        self.job_size = len(self.cut_list)


class Layout(object):
    """
    A layout contains the packed job of one color and thickness.
    """

    def __init__(self, color, thickness, job, panels):
        self.color = color
        self.thickness = thickness
        self.layout = layout_jobs(job, panels)
        self.num_panels = len(self.layout)


def create_job_list(order_list):
    """
    Takes in an order list, which is a combo of designs and quantities. Splits all  designs into jobs based on material color and thickness. Returns the job list, which has a Job object for all layers of one color/thickness combination.
    """

    job_list = []

    for d in order_list:
        design = d[0]
        count = d[1]

        for z in range(count):

            for lg in design.layer_groups:

                if (len(job_list) == 0):
                    # Job list is empty, create job.
                    new_job = Job(lg.color, lg.thickness, lg.layers)
                    job_list.append(new_job)

                else:
                    for j in job_list:
                        # Does a job already exist?
                        if (j.color == lg.color and j.thickness == lg.thickness):
                            j.update_cut_list(lg.layers)
                            break

                    else:
                        # No matches, need new job.
                        new_job = Job(lg.color, lg.thickness, lg.layers)
                        job_list.append(new_job)
    return(job_list)


def layout_jobs(job, panels):
    layout = newPacker()

    # Add the design layers to packing queue
    for j in job:
        layout.add_rect(*j)

    # Add available panles to packing queue
    for p in panels:
        layout.add_bin(*p)

    layout.pack()
    return layout


def create_layouts_list(job_list, material_list):
    # as long as we have jobs left:
    layouts_list = []
    while (len(job_list) > 0):
        current_job = job_list.pop()  # grab a job

        # match it up with the correct layers
        for m in range(len(material_list)):
            if(material_list[m].color == current_job.color and material_list[m].thickness == current_job.thickness):
                current_material = material_list.pop(m)
                new_layout = Layout(
                    current_material.color, current_material.thickness, current_job.cut_list, current_material.cut_list)
                layouts_list.append(new_layout)
                break

        else:
            print("no matching material available for job: {0}, {1}mm".format(
                current_job.color, current_job.thickness))

    return layouts_list


def plot_layouts(layout_list):
    """
    1. Go through each bin in the packer. Create a plot, with xy dims given by the bin dimensions, and name the plot after the bin number.
    2. For each rect in the bin, add a square to the plot.
    3. Close the figure when done
    """

    for l in layout_list:
        layout = l.layout
        num_bins = len(layout)
        num_rows = max(1, np.rint(np.sqrt(num_bins)))
        num_cols = int(max(1, np.ceil(num_bins / num_rows)))

        fig = plt.figure()

        # heads up, you need to convert from dec to float to use mpl...
        for abin in range(len(layout)):

            # print("BIN: width {0} height {1}".format(
            #     layout[abin].width, layout[abin].height))
            width = float(layout[abin].width)
            height = float(layout[abin].height)

            ax = fig.add_subplot(num_rows, num_cols, abin + 1, aspect='equal')
            ax.set_title("Panel {0} ({1}'',{2}'')".format(
                str(abin + 1), str(width), str(height)))
            ax.set_xbound(0, width)
            ax.set_ybound(0, height)
            ax.set_xticks(np.linspace(0, width, 3))
            ax.set_yticks(np.linspace(0, height, 3))

            # Star adding rects
            for rect in layout[abin]:
                ax.add_patch(
                    patches.Rectangle(
                        (rect.x, rect.y),  # (x,y)
                        rect.width,  # width
                        rect.height,  # height
                        edgecolor="black",
                        facecolor=l.color,
                        linewidth=1,
                    )
                )
        fig.suptitle("Acrylic: Color {0}, {1}mm".format(
            l.color, l.thickness))
        fig.subplots_adjust(hspace=1)
    plt.show()

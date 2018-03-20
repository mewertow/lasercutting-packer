from rectpack import newPacker, float2dec
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from time import sleep


class Job(object):
    """
    A job is intended to be run on one type of material, hence thickness and color and material should be fixed. It contains all the portions from all designs that fit that specification.
    """

    def __init__(self, color, thickness, cut_list=[]):
        self.color = color
        self.thickness = thickness
        self.cut_list = cut_list[:]
        self.job_size = len(self.cut_list)

    def update_cut_list(self, new_cuts):
        # new cuts is a list of cuts, passed from another object...
        print("\n adding new cuts: {0}, size {1}".format(
            new_cuts, len(new_cuts)))
        # print("id of new cuts: {0}".format(id(new_cuts)))
        # print("id of self.cut_list: {0}".format(id(self.cut_list)))
        self.cut_list.extend(new_cuts[:])
        print("new cut list: {0} \n".format(self.cut_list))

        self.job_size = len(self.cut_list)

    # def get_job_size():
    #     return len(self.cut_list)


def create_job_list(order_list):
    """
    Takes in an order list, which is a combo of designs and quantities. Splits all  designs into jobs based on material color and thickness. Creates the job list, which has one Job object that contains all layers for that color and thickness.
    """

    job_list = []

    for d in order_list:
        design = d[0]
        count = d[1]
        print("\n COPIES OF DESIGN, TOTAL: {0}\n".format(count))
        print("Layer groups to check from design: {0}".format(
            design.layer_groups))

        # Go through each layer group in each design, and look at it's color/thickness.
        # Based on these parameters, either create a new job (if unique) or append a job (if exists)
        for z in range(count):
            print("current jobs in list: {0}".format(job_list))
            print("COUNT: {0} out of {1} COPIES".format(z + 1, count))

            for lg in design.layer_groups:
                # print(
                #     "\n checking for {0} acrylic, {1} mm...".format(lg.color, lg.thickness))
                # print("job_list = {0}".format((job_list)))

                # if our job list is empty, of course we just create a new job and add to Job list.
                if (len(job_list) == 0):

                    new_job = Job(lg.color, lg.thickness, lg.layers)
                    job_list.append(new_job)

                    print("EMPTY LIST. Created job for {0} acrylic at {1} mm thickness. Adding {2} cuts for total of {3}. Full CUT list:  {4}\n".format(
                        new_job.color, new_job.thickness, len(lg.layers), new_job.job_size, new_job.cut_list))

                else:
                    for j in job_list:
                        print("checking against job {0}, {1} acrylic, {2} mm".format(
                            j, j.color, j.thickness))
                        # # check - can we append this layer group to existing job?
                        if (j.color == lg.color and j.thickness == lg.thickness):
                            print("EXISTING JOB FOUND!")
                            j.update_cut_list(lg.layers)
                            print("UPDATED Job for {0} acrylic at {1} mm thickness, added {2} cuts for total of {3} cuts. Full CUT list: {4}\n".format(
                                j.color, j.thickness, len(lg.layers), j.job_size, j.cut_list))
                            # print("break, updated")
                            break

                    else:
                        # no matches...
                        new_job = Job(lg.color, lg.thickness, lg.layers)
                        job_list.append(new_job)
                        print("NEW JOB CREATED for {0} acrylic at {1} mm thickness. Adding {2} cuts for total {3}. Full CUT list: {4}\n".format(
                            new_job.color, new_job.thickness, len(lg.layers), new_job.job_size, new_job.cut_list))


def layout_job(job, panels):
    layout = newPacker()

    # Add the design layers to packing queue
    for j in job:
        layout.add_rect(*j)

    # Add available panles to packing queue
    for p in panels:
        layout.add_bin(*p)

    layout.pack()

    return layout


def plot_layouts(layout):
    """
    1. Go through each bin in the packer. Create a plot, with xy dims given by the bin dimensions, and name the plot after the bin number.
    2. For each rect in the bin, add a square to the plot.
    3. Close the figure when done
    """
    num_bins = len(layout)
    print("num_bins = {0}".format(num_bins))
    num_cols = max(1, np.rint(np.sqrt(num_bins)))
    print("num cols = {0}".format(num_cols))
    num_rows = max(1, np.rint(num_bins / num_cols))
    print("num_rows = {0}".format(num_rows))

    fig = plt.figure()

    for abin in range(len(layout)):

        ax = fig.add_subplot(num_rows, num_cols, abin + 1, aspect='equal')
        ax.set_title("Panel {0} ({1}'',{2}'')".format(
            str(abin), str(layout[abin].width), str(layout[abin].height)))
        ax.set_xbound(0, layout[abin].width)
        ax.set_ybound(0, layout[abin].height)
        ax.set_xticks(np.linspace(0, layout[abin].width, 3))
        ax.set_yticks(np.linspace(0, layout[abin].height, 3))

        # Star adding rects
        for rect in layout[abin]:
            ax.add_patch(
                patches.Rectangle(
                    (rect.x, rect.y),  # (x,y)
                    rect.width,  # width
                    rect.height,  # height
                    edgecolor="black",
                    linewidth=1,
                )
            )
    fig.suptitle("Cutting Layout")
    fig.subplots_adjust(hspace=1)
    plt.show()

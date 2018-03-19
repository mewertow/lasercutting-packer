from rectpack import newPacker, float2dec
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def create_job(design_list):
    """
    design_list should be list of tuples of (design, quantity).
    Returns list of tuples of all the individual layers to cut out of the panel w/ x-y dims.
    """
    job = []
    for x in design_list:  # Start by iterating over each item in the design list
        for i in range(x[1]):  # For number of copies of the design
            for j in x[0].layers:  # individually append each layer
                job.append(j)
    return job


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

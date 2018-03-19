from jobs import *
from rectpack import float2dec


class Design(object):
    """
    Combination of sheets in various colors and thicknesses.
    """

    def __init__(self, *design_specs):
        # Take your input tuples and convert them to0 LayerGroup objects.

        # print("params = {0}".format(design_specs))
        self.layer_groups = self.list_groups(design_specs)
        self.num_groups = len(self.layer_groups)

        # print(self.layer_groups)

    def list_groups(self, specs):
        """
        Makes a list of the layer groups for this design.
        """
        glist = []
        # print("specs = {}".format(specs))
        for sp in specs:
            group = LayerGroup(*sp)
            # print(group.color)
            glist.append(group)
        return glist


class LayerGroup(object):
    """
    Specification for some number of identical sheets.
    """

    def __init__(self, color, thickness, length, width, num_panels, buffer):
        # Automatically adds desired buffer to each dimension for sanity

        self.color = color  # string
        self.thickness = thickness  # mm
        self.length = float2dec(length + buffer, 2)
        self.width = float2dec(width + buffer, 2)
        self.num_panels = num_panels
        self.layers = self.list_layers()

    def list_layers(self):
        """Creates a list of the layers required for the design."""
        llist = []
        for x in range(self.num_panels):
            llist.append((self.length, self.width))
        return llist


def list_panels(*args):
    """Take in desired panels, make string"""
    # Args must by a list of tuples, where each is (width, height, num)
    plist = []
    for panel in args:
        for x in range(panel[2]):
            plist.append((panel[0], panel[1]))
    return plist


# In inches: (Color, Thickness, Width, Height, NumLayers, Buffer) list of lists
TEST1 = Design(
    ("blue", 1, 1, 1, 1, 0),
    ("Orange", 1, 1, 1, 1, 0),
    ("red", 2, 2, 2, 2, 0),
)

TEST2 = Design(
    ("black", 4, 3, 3, 3, 0),
    ("blue", 1, 4, 4, 4, 0)
    # ("ORANGE", 1, 4, 4, 4, 0)
)

ORDER_LIST = [
    (TEST1, 1),
    (TEST2, 1),
]


job_list = []

for d in ORDER_LIST:
    design = d[0]
    count = d[1]
    # Go through each layer group in each design, and look at it's color/thickness.
    # Based on these parameters, either create a new job (if unique) or append a job (if exists)
    print("layer groups to check: {0}".format(design.layer_groups))
    for lg in design.layer_groups:
        print(
            "checking for {0} acrylic, {1} mm...".format(lg.color, lg.thickness))
        print("job_list = {0}".format((job_list)))

        # if our job list is empty, of course we just create a new job and add to Job list.
        if (len(job_list) == 0):

            new_job = Job(lg.color, lg.thickness, lg.layers)
            job_list.append(new_job)

            print("EMPTY LIST. Created job for {0} acrylic at {1} mm thickness. Adding {2} cuts for total of {3}. Full CUT list: \n {4}".format(
                new_job.color, new_job.thickness, len(lg.layers), new_job.job_size, new_job.cut_list))

        else:
            for j in job_list:
                print("checking against job {0}, {1} acrylic, {2} mm".format(
                    j, j.color, j.thickness))
                # check - can we append this layer group to existing job?
                if (j.color == lg.color and j.thickness == lg.thickness):
                    j.update_cut_list(lg.layers)
                    print("UPDATED Job for {0} acrylic at {1} mm thickness, added {2} cuts for total of {3} cuts. Full CUT list: \n {4}".format(
                        j.color, j.thickness, len(lg.layers), j.job_size, j.cut_list))
                    print("break, updated")
                    break

            else:
                # no matches...
                new_job = Job(lg.color, lg.thickness, lg.layers)
                job_list.append(new_job)
                print("NEW JOB CREATED for {0} acrylic at {1} mm thickness. Adding {2} cuts for total {3}. Full CUT list: \n {4}".format(
                    new_job.color, new_job.thickness, len(lg.layers), new_job.job_size, new_job.cut_list))

            # for i in x:
            #     for j in xrange(i[1]):

            # for lg in range(DESIGN_LIST[d].num_groups):
            #     print("Group {0} has color {1} and layers: \n {2}".format(
            #         lg, DESIGN_LIST[d].layer_groups[lg].color, DESIGN_LIST[d].layer_groups[lg].layers))

            # LAYERBOX = Design(14.3, 8.7, 11, 0.4)
            # ECONOMYBOX = Design(10.5, 8.0, 2, 0.4)
            # MINIHITBOX = Design(11.8, 5.9, 6, 0.4)
            # BLANKPANEL = Design(28, 14, 1, 0)
            # FULLPANEL = Design(49, 96, 1, 0)

            # Each tuple should be design_name, num_copies
            # DESIGN_LIST = [(LAYERBOX, 1), (MINIHITBOX, 1),
            #                (ECONOMYBOX, 1), (BLANKPANEL, 1)]
            #

            # DESIGN_LIST = [(TEST, 1)]
            #
            # PANEL_LIST = list_panels((10, 10, 2))
            # #
            # # ORDER MATTERS in panel list. List the panels you'd rather fill first.
            # print(PANEL_LIST)
            #
            #
            # JOBS = create_job(DESIGN_LIST)
            # LAYOUTS = layout_job(JOBS, PANEL_LIST)
            # plot_layouts(LAYOUTS)

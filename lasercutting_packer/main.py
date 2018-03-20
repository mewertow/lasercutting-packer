from jobs import *
from rectpack import float2dec


class Design(object):
    """
    Combination of sheets in various colors and thicknesses.
    """

    def __init__(self, *design_specs):
        # Take your input tuples and convert them to0 LayerGroup objects.

        self.layer_groups = self.list_groups(design_specs)
        self.num_groups = len(self.layer_groups)

    def list_groups(self, specs):
        """
        Makes a list of the layer groups for this design.
        """
        glist = []
        for sp in specs:
            group = LayerGroup(*sp)
            glist.append(group)
        return glist


class LayerGroup(object):
    """
    Specification for some number of identical sheets.
    """

    def __init__(self, color, thickness, length, width, num_panels, buffer):
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


# Job Designs -------------------------

# In inches: (Color, Thickness, Width, Height, NumLayers, Buffer) list of lists
TEST1 = Design(
    ("blue", 6, 1, 1, 1, 0),
    # ("Orange", 1, 1, 1, 1, 0),
    # ("red", 2, 2, 2, 2, 0),
)

TEST2 = Design(
    ("black", 6, 3, 3, 3, 0),
    ("black", 6, 2, 2, 3, 0),
    # ("blue", 1, 4, 4, 4, 0),
    ("orange", 1, 4, 4, 4, 0)
)

# LAYERBOX = Design(14.3, 8.7, 11, 0.4)
# ECONOMYBOX = Design(10.5, 8.0, 2, 0.4)
# MINIHITBOX = Design(11.8, 5.9, 6, 0.4)

# Job Designs -------------------------
# SMALLPANEL_BLUE = Design(("blue", 6, 28, 14, 1, 0))
# FULLPANEL_BLUE = Design(("blue", 6, 49, 96, 1, 0))
# SMALLPANEL_BLACK = Design(("black", 6, 28, 14, 1, 0))
# FULLPANEL_BLACK = Design(("black", 6, 49, 96, 1, 0))

SMALLPANEL_BLUE = Design(("blue", 6, 10, 10, 1, 0))
FULLPANEL_BLUE = Design(("blue", 6, 25, 25, 1, 0))
SMALLPANEL_BLACK = Design(("black", 6, 10, 10, 1, 0))
FULLPANEL_BLACK = Design(("black", 6, 25, 25, 1, 0))


ORDER_LIST = [
    (TEST1, 2),
    (TEST2, 1),
]

PANEL_LIST = [
    (SMALLPANEL_BLUE, 2),
    # (FULLPANEL_BLACK, 1),
    (FULLPANEL_BLACK, 1),
    # (FULLPANEL_BLUE, 1)
]


JOB_LIST = create_job_list(ORDER_LIST)
# print("\nlayer types to cut: {0}".format(JOB_LIST))
# print("layers: ")
# for j in JOB_LIST:
#     print("color {0}, thickness {1}, {2} cuts: {3}".format(
#         j.color, j.thickness, len(j.cut_list), j.cut_list))
# now, need to use same idea to create Panel List, where we spec the types of panels we have.pooooooooooooooppp

MATERIAL_LIST = create_job_list(PANEL_LIST)
# print("\npanels types to use: {0}".format(JOB_LIST))
# print("panels: ")
# for p in PANEL_LIST:
#     print("color {0}, thickness {1}, {2} cuts: {3}".format(
#         p.color, p.thickness, len(p.cut_list), p.cut_list))

plot_job_layouts(JOB_LIST, MATERIAL_LIST)


# print(PANEL_LIST)
# for j in PANEL_LIST:
#     print(j.color)

# PANEL_LIST = list_panels((10, 10, 2))
# #
# # ORDER MATTERS in panel list. List the panels you'd rather fill first.
# print(PANEL_LIST)
#
#
# LAYOUTS = layout_job(JOBS, PANEL_LIST)
# plot_layouts(LAYOUTS)

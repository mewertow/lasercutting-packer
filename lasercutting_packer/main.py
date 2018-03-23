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
# In inches: (Color, Thickness[mm], Width[in], Height[in], NumLayers, Buffer) list of lists

LAYERBOX = Design(
    ("none", 6, 14.3, 8.7, 11, 0.4),  # main
    ("none", 3, 14.3, 8.7, 1, 0.4),  # art cover
    ("red", 6, 11.4, 2.1, 2, 0.4),  # frontpanel
    ("none", 6, 11.9, 1.7, 2, 0.4),  # frontpanel2
    ("black", 6, 5.9, 2.1, 2, 0.4),  # sidepanel
    ("none", 6, 6.4, 1.7, 2, 0.4))  # sidepanel2


ECONOMYBOX = Design(
    ("none", 6, 10.5, 8.0, 2, 0.4),  # main
    ("none", 3, 10.5, 8.0, 2, 0.4),  # art cover
    ("none", 6, 1.9, 1.2, 6, 0.4))  # side insert

MINIHITBOX = Design(
    ("clear", 6, 11.8, 5.9, 6, 0.4))

# Job Designs -------------------------

# TEST_PANEL = Design(("blue", 6, 4, 2, 1, 0))
SMALLPANEL_BLUE_6 = Design(("blue", 6, 18, 24, 1, 0))
FULLPANEL_BLUE_6 = Design(("blue", 6, 48, 96, 1, 0))

SMALLPANEL_BLACK_6 = Design(("black", 6, 18, 24, 1, 0))
FULLPANEL_BLACK_6 = Design(("black", 6, 48, 96, 1, 0))

SMALLPANEL_CLEAR_6 = Design(("none", 6, 18, 24, 1, 0))
FULLPANEL_CLEAR_6 = Design(("none", 6, 48, 96, 1, 0))
SMALLPANEL_CLEAR_3 = Design(("none", 3, 18, 24, 1, 0))
FULLPANEL_CLEAR_3 = Design(("none", 3, 48, 96, 1, 0))

SMALLPANEL_RED_6 = Design(("red", 6, 18, 24, 1, 0))
FULLPANEL_RED_6 = Design(("red", 6, 48, 96, 1, 0))
SMALLPANEL_RED_3 = Design(("red", 3, 18, 24, 1, 0))
FULLPANEL_RED_3 = Design(("red", 3, 48, 96, 1, 0))


DESIGN_LIST = [
    (LAYERBOX, 5)
    # (ECONOMYBOX, 5)
    # (TEST2, 1),
]

PANEL_LIST = [
    # (TEST_PANEL, 1),
    # (SMALLPANEL_BLUE, 2),
    # (FULLPANEL_BLACK, 1),
    (FULLPANEL_CLEAR_6, 10),
    (SMALLPANEL_RED_6, 10),
    (SMALLPANEL_RED_3, 10),

    (SMALLPANEL_BLACK_6, 10),
    (FULLPANEL_RED_6, 29),
    # (FULLPANEL_CLEAR_3, 20)
    # (SMALLPANEL_CLEAR_3, 2)

    # (FULLPANEL_BLUE, 1)
]


JOB_LIST = create_job_list(DESIGN_LIST)

MATERIAL_LIST = create_job_list(PANEL_LIST)

LAYOUTS_LIST = create_layouts_list(JOB_LIST, MATERIAL_LIST)

# print(len(LAYOUTS_LIST[0].layout))
# plot_job_layouts(JOB_LIST, MATERIAL_LIST)
plot_layouts(LAYOUTS_LIST)


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

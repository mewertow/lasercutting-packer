from jobs import *
from rectpack import float2dec


class Design(object):
    """
    Combination of sheets in various colors and thicknesses.
    """

    def __init__(self, length, width, num_panels, buffer):
        # Automatically adds 10mm (0.4in) to each dimension for sanity

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


# In inches: (Thickness, Width, Height, NumLayers, Buffer) list of lists
LAYERBOX = Design(14.3, 8.7, 11, 0.4)
ECONOMYBOX = Design(10.5, 8.0, 2, 0.4)
MINIHITBOX = Design(11.8, 5.9, 6, 0.4)
BLANKPANEL = Design(28, 14, 1, 0)

# Each tuple should be design_name, num_copies
DESIGN_LIST = [(LAYERBOX, 1), (MINIHITBOX, 1),
               (ECONOMYBOX, 1), (BLANKPANEL, 1)]

PANEL_LIST = list_panels((48, 96, 1), (24, 18, 20))
#
# ORDER MATTERS in panel list. List the panels you'd rather fill first.
print(PANEL_LIST)


JOB = create_job(DESIGN_LIST)
LAYOUT = layout_job(JOB, PANEL_LIST)
plot_layouts(LAYOUT)

from jobs import *


class Design(object):
    """Combination of sheets in various colors and thicknesses"""

    def __init__(self, length, width, num_panels):
        self.length = length
        self.width = width
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


LAYERBOX = Design(15, 9, 11)
ECONOMYBOX = Design(11, 9, 2)
MINIHITBOX = Design(12, 6, 6)
BLANKPANEL = Design(28, 14, 1)

# Each tuple should be design_name, num_copies
DESIGN_LIST = [(LAYERBOX, 2), (MINIHITBOX, 1),
               (ECONOMYBOX, 2), (BLANKPANEL, 1)]

PANEL_LIST = list_panels((48, 96, 1), (24, 18, 4))
# ORDER MATTERS in panel list. List the panels you'd rather fill first.
print(PANEL_LIST)


JOB = create_job(DESIGN_LIST)
LAYOUT = layout_job(JOB, PANEL_LIST)
plot_layouts(LAYOUT)

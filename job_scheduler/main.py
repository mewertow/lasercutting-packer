from panelfitting.jobs import *


class Design(object):
    """Combination of sheets in various colors and thicknesses"""

    def __init__(self, length, width, num_panels):
        self.length = length
        self.width = width
        self.num_panels = num_panels
        self.layers = self.list_layers()

    def list_layers(self):
        """Creates a list of the sheets as layers."""
        llist = []
        for x in range(self.num_panels):
            llist.append((self.length, self.width))
        return llist


LAYERBOX = Design(15, 9, 11)
ECONOMYBOX = Design(11, 9, 2)
MINIHITBOX = Design(12, 6, 6)

DESIGN_LIST = [(LAYERBOX, 1), (MINIHITBOX, 1), (ECONOMYBOX, 1)]
JOB = create_job(DESIGN_LIST)

PANELS = [(48, 96), (48, 96)]

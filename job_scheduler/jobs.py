from rectpack import newPacker
import matplotlib.pyplot as plt
import numpy as np


def create_job(design_list):
    """
    design_list should be list of tuples of (design, quantity)
    Job should be a list of tuples of all the individual layers to cut out of the panel w/ x-y dims.
    """
    job = []
    for x in design_list:  # Start by iterating over each item in the design list
        for i in range(x[1]):  # For number of copies of the design
            for j in x[0].layers:  # individually append each layer
                job.append(j)
    return job

#
# def pack_job(job, panels):

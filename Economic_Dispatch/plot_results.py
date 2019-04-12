# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 15:53:54 2019

@author: Asun
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_results(model):
    x = np.arange(0, 3)
    y = [model.flow[generating_unit,1].value for generating_unit in model.indexes_generating_units]
    plt.plot(x, y, color = 'red', marker = 'o', linestyle = "--")
    plt.savefig('flow_plot.pdf')
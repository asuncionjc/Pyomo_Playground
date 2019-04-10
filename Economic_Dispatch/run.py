# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:59:09 2019

@author: Asun
"""

from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pyomo.environ as pe


# Extra packages
import os
path = 'C:/Users/Asun/Github/Pyomo_Playground/Economic_Dispatch'
os.chdir(path)

from data import *
from model import *

model = create_model(number_of_time_periods,
                     number_of_generating_units,
                     number_of_nodes,
                     number_of_lines,
                     generating_units_cost,
                     demand,
                     lower_bound_power,
                     upper_bound_power,
                     maximum_flow,
                     lower_bound_ramping,
                     upper_bound_ramping)
#model.pprint()
solver = SolverFactory("cplex")
results = solver.solve(model,
                      tee = True)

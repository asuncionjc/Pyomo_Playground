# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:12:06 2019

@author: Asun
"""

from __future__ import division
from pyomo.environ import *

model = AbstractModel()

#Parameters

model.number_of_time_periods = Param(within = NonNegativeIntegers)
model.number_of_generating_units = Param(within = NonNegativeIntegers)
model.number_of_nodes = Param(within = NonNegativeIntegers)
model.number_of_lines = Param(within = NonNegativeIntegers)

model.indexes_time_periods = RangeSet(1, 
                                      model.number_of_time_periods)
model.indexes_generation_units = RangeSet(1, 
                                          model.number_of_generating_units)
model.indexes_nodes = RangeSet(1, 
                               model.number_of_nodes)
model.indexes_lines = RangeSet(1, 
                               model.number_of_lines)

model.generating_units_cost = Param(model.indexes_generation_units,
                                    within = NonNegativeReals)
model.demand = Param(model.indexes_lines,
                     model.indexes_time_periods,
                     within = NonNegativeReals)
model.lower_bound_power = Param(model.indexes_generating_units,
                                within = NonNegativeReals)
model.upper_bound_power = Param(model.indexes_generating_units,
                                within = NonNegativeReals)
model.maximum_flow = Param(model.indexes_lines,
                           model.indexes_time_periods,
                           within = NonNegativeReals)
model.lower_bound_ramping = Param(model.indexes_generating_units,
                                  within = NonNegativeReals)
model.upper_bound_ramping = Param(model.indexes_generating_units,
                                  within = NonNegativeReals)

#Decision variables

model.power_generating_units = Var(model.indexes_generating_units,
                                   model.indexes_time_periods)
model.flow = Var(model.indexes_lines,
                 model.indexes_time_periods)

























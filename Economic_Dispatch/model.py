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
model.indexes_time_periods_except_first = RangeSet(2, 
                                                   model.number_of_time_periods)
model.indexes_generating_units = RangeSet(1, 
                                          model.number_of_generating_units)
model.indexes_nodes = RangeSet(1, 
                               model.number_of_nodes)
model.indexes_lines = RangeSet(1, 
                               model.number_of_lines)

model.generating_units_cost = Param(model.indexes_generating_units,
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

# Objective function

def total_generating_cost(model):
    objective_value = sum(sum(model.generating_units_cost[generating_unit]*model.power_generating_units[generating_unit, time_period] for generating_unit in model.indexes_generating_units) for time_period in model.indexes_time_periods)
    return objective_value

model.OBJ = Objective(rule = total_generating_cost)

# Constraints

def lower_bound_generating_power(model,
                                 generating_unit,
                                 time_period):
    constraint = model.power_generating_units[generating_unit, time_period] >= model.lower_bound_power[generating_unit]
    return(constraint)
model.lower_bound_generating_power_constraint = Constraint(model.indexes_generating_units,
                                                           model.indexes_time_periods,
                                                           rule = lower_bound_generating_power)

def upper_bound_generating_power(model,
                                 generating_unit,
                                 time_period):
    constraint = model.power_generating_units[generating_unit, time_period] <= model.upper_bound_power[generating_unit]
    return(constraint)
model.upper_bound_generating_power_constraint = Constraint(model.indexes_generating_units,
                                                           model.indexes_time_periods,
                                                           rule = upper_bound_generating_power)

#def power_balance(model,
#                  node,
#                  time_period):
#    constraint = sum() == model.demand[node, time_period] + sum() - sum()
#    return(constraint)
#model.power_balance_constraint = Constraint(model.indexes_nodes,
#                                            model.indexes_time_periods,
#                                            rule = power_balance)

def lower_bound_flow(model,
                     line,
                     time_period):
    constraint = model.flow[line, time_period] >= - model.maximum_flow[line, time_period]
    return(constraint)
model.lower_bound_flow_constraint = Constraint(model.indexes_lines,
                                               model.indexes_time_periods,
                                               rule = lower_bound_flow)

def upper_bound_flow(model,
                     line,
                     time_period):
    constraint = model.flow[line, time_period] <= model.maximum_flow[line, time_period]
    return(constraint)
model.upper_bound_flow_constraint = Constraint(model.indexes_lines,
                                               model.indexes_time_periods,
                                               rule = upper_bound_flow)

def lower_bound_ramping(model,
                        generating_unit,
                        time_period):
    constraint = model.power_generating_units[generating_unit, time_period] - model.power_generating_units[generating_unit, time_period - 1] >= model.lower_bound_ramping[generating_unit]
    return(constraint)
model.lower_bound_ramping_constraint = Constraint(model.indexes_generating_units,
                                                  model.indexes_time_periods_except_first,
                                                  rule = lower_bound_ramping)

def upper_bound_ramping(model,
                        generating_unit,
                        time_period):
    constraint = model.power_generating_units[generating_unit, time_period] - model.power_generating_units[generating_unit, time_period - 1] <= model.upper_bound_ramping[generating_unit]
    return(constraint)
model.upper_bound_ramping_constraint = Constraint(model.indexes_generating_units,
                                                  model.indexes_time_periods_except_first,
                                                  rule = upper_bound_ramping)




























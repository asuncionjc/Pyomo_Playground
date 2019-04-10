# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:12:06 2019

@author: Asun
"""

from __future__ import division
import pyomo.environ as pe

def create_model():
    m = pe.ConcreteModel()
    
    # Sets
    m.indexes_time_periods = pe.RangeSet(number_of_time_periods)
    m.indexes_time_periods_except_first = pe.RangeSet(2, 
                                                      number_of_time_periods)
    m.indexes_generating_units = pe.RangeSet(number_of_generating_units)
    m.indexes_nodes = pe.RangeSet(number_of_nodes)
    m.indexes_lines = pe.RangeSet(number_of_lines)
    
    #Decision variables
    m.power_generating_units = pe.Var(m.indexes_generating_units,
                                      m.indexes_time_periods)
    m.flow = pe.Var(m.indexes_lines,
                    m.indexes_time_periods)
    
    # Objective function
    def total_generating_cost(m):
    objective_value = sum(sum(generating_units_cost[generating_unit - 1]*m.power_generating_units[generating_unit, time_period] for generating_unit in m.indexes_generating_units) for time_period in m.indexes_time_periods)
    return objective_value

    m.OBJ = Objective(rule = total_generating_cost,
                      sense = pe.minimize)
    
    # Constraints

    def lower_bound_generating_power(m,
                                     generating_unit,
                                     time_period):
    constraint = m.power_generating_units[generating_unit, time_period] >= lower_bound_power[generating_unit - 1]
    return(constraint)
    m.lower_bound_generating_power_constraint = Constraint(m.indexes_generating_units,
                                                           m.indexes_time_periods,
                                                           rule = lower_bound_generating_power)

    def upper_bound_generating_power(m,
                                     generating_unit,
                                     time_period):
    constraint = m.power_generating_units[generating_unit, time_period] <= upper_bound_power[generating_unit - 1]
    return(constraint)
    m.upper_bound_generating_power_constraint = Constraint(m.indexes_generating_units,
                                                           m.indexes_time_periods,
                                                           rule = upper_bound_generating_power)
    #def power_balance(m,
    #                  node,
    #                  time_period):
    #    constraint = sum() == demand[node, time_period] + sum() - sum()
    #    return(constraint)
    #m.power_balance_constraint = Constraint(m.indexes_nodes,
    #                                        m.indexes_time_periods,
    #                                        rule = power_balance)

    def lower_bound_flow(m,
                         line,
                         time_period):
        constraint = m.flow[line, time_period] >= - maximum_flow[line - 1, time_period - 1]
        return(constraint)
    m.lower_bound_flow_constraint = Constraint(m.indexes_lines,
                                               m.indexes_time_periods,
                                               rule = lower_bound_flow)
    
    def upper_bound_flow(m,
                         line,
                         time_period):
        constraint = m.flow[line, time_period] <= maximum_flow[line - 1, time_period - 1]
        return(constraint)
    m.upper_bound_flow_constraint = Constraint(m.indexes_lines,
                                               m.indexes_time_periods,
                                               rule = upper_bound_flow)
    
    def lower_bound_ramping(m,
                            generating_unit,
                            time_period):
        constraint = m.power_generating_units[generating_unit, time_period] - m.power_generating_units[generating_unit, time_period - 1] >= lower_bound_ramping[generating_unit - 1]
        return(constraint)
    m.lower_bound_ramping_constraint = Constraint(m.indexes_generating_units,
                                                  m.indexes_time_periods_except_first,
                                                  rule = lower_bound_ramping)
    
    def upper_bound_ramping(model,
                            generating_unit,
                            time_period):
        constraint = m.power_generating_units[generating_unit, time_period] - m.power_generating_units[generating_unit, time_period - 1] <= upper_bound_ramping[generating_unit - 1]
        return(constraint)
    m.upper_bound_ramping_constraint = Constraint(m.indexes_generating_units,
                                                  m.indexes_time_periods_except_first,
                                                  rule = upper_bound_ramping)

    return m



































# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:12:06 2019

@author: Asun
"""

from __future__ import division
import pyomo.environ as pe
from pyomo.opt.base import SolverFactory
import logging

def model(data,
          config):
    
    m = pe.ConcreteModel()
    
    #Encapsulate the data
    m.number_of_time_periods = data['number_of_time_periods']
    m.number_of_generating_units = data['number_of_generating_units']
    m.number_of_nodes = data['number_of_nodes']
    m.number_of_lines = data['number_of_lines']
    
    m.generating_units_cost = data['generating_units_cost']
    m.demand = data['demand']
    
    m.lower_bound_power = data['lower_bound_power']
    m.upper_bound_power = data['upper_bound_power']
    
    m.maximum_flow = data['maximum_flow']
    
    m.lower_bound_ramping = data['lower_bound_ramping']
    m.upper_bound_ramping = data['upper_bound_ramping']
    
    m.origin_node_line_relationship = data['origin_node_line_relationship']
    m.end_node_line_relationship = data['end_node_line_relationship']
    
    
    
    # Sets
    m.indexes_time_periods = pe.RangeSet(m.number_of_time_periods)
    m.indexes_time_periods_except_first = pe.RangeSet(2, 
                                                      m.number_of_time_periods)
    m.indexes_generating_units = pe.RangeSet(m.number_of_generating_units)
    m.indexes_nodes = pe.RangeSet(m.number_of_nodes)
    m.indexes_lines = pe.RangeSet(m.number_of_lines)
    
    #Decision variables
    m.power_generating_units = pe.Var(m.indexes_generating_units,
                                      m.indexes_time_periods)
    m.flow = pe.Var(m.indexes_lines,
                    m.indexes_time_periods)
    
    # Objective function
    m.OBJ = pe.Objective(rule = total_generating_cost,
                         sense = pe.minimize)
    
    # Constraints

    
    m.lower_bound_generating_power_constraint = pe.Constraint(m.indexes_generating_units,
                                                              m.indexes_time_periods,
                                                              rule = lower_bound_generating_power)

    m.upper_bound_generating_power_constraint = pe.Constraint(m.indexes_generating_units,
                                                           m.indexes_time_periods,
                                                           rule = upper_bound_generating_power)
    m.power_balance_constraint = pe.Constraint(m.indexes_nodes,
                                               m.indexes_time_periods,
                                               rule = power_balance)
    
    m.lower_bound_flow_constraint = pe.Constraint(m.indexes_lines,
                                                  m.indexes_time_periods,
                                                  rule = lower_bound_flow)
    
    m.upper_bound_flow_constraint = pe.Constraint(m.indexes_lines,
                                                  m.indexes_time_periods,
                                                  rule = upper_bound_flow)
    
    m.lower_bound_ramping_constraint = pe.Constraint(m.indexes_generating_units,
                                                     m.indexes_time_periods_except_first,
                                                     rule = lower_bound_ramping_limit)
        

    m.upper_bound_ramping_constraint = pe.Constraint(m.indexes_generating_units,
                                                     m.indexes_time_periods_except_first,
                                                     rule = upper_bound_ramping_limit)
    
    logging.info("Model prepared")

    return m


#Objective function
def total_generating_cost(m):
        return sum(sum(m.generating_units_cost[generating_unit - 1]*m.power_generating_units[generating_unit, time_period] for generating_unit in m.indexes_generating_units) for time_period in m.indexes_time_periods)
     

#Constraints

def lower_bound_generating_power(m,
                                 generating_unit,
                                 time_period):
        return m.power_generating_units[generating_unit, time_period] >= m.lower_bound_power[generating_unit - 1]
    
def upper_bound_generating_power(m,
                                 generating_unit,
                                 time_period):
        return m.power_generating_units[generating_unit, time_period] <= m.upper_bound_power[generating_unit - 1]
    

def power_balance(m,
                  node,
                  time_period):
        constraint = sum(m.power_generating_units[generating_unit, time_period] for generating_unit in m.indexes_generating_units) == m.demand[node - 1, time_period - 1] + sum(m.origin_node_line_relationship[node - 1, line - 1]*m.flow[line, time_period] for line in m.indexes_lines) - sum(m.end_node_line_relationship[node - 1, line - 1]*m.flow[line, time_period] for line in m.indexes_lines)
        return(constraint)
    

def lower_bound_flow(m,
                     line,
                     time_period):
        return m.flow[line, time_period] >= - m.maximum_flow[line - 1, time_period - 1]
    

def upper_bound_flow(m,
                     line,
                     time_period):
      return m.flow[line, time_period] <= m.maximum_flow[line - 1, time_period - 1]
    

def lower_bound_ramping_limit(m,
                              generating_unit,
                              time_period):
        return m.power_generating_units[generating_unit, time_period] - m.power_generating_units[generating_unit, time_period] >= m.lower_bound_ramping[generating_unit - 1]
    

def upper_bound_ramping_limit(m,
                              generating_unit,
                              time_period):
        return m.power_generating_units[generating_unit, time_period] - m.power_generating_units[generating_unit, time_period - 1] <= m.upper_bound_ramping[generating_unit - 1]
    

#Processing
        
def run_solver(instance,
               conf):
    
    solver = SolverFactory(conf['solver'])
    results = solver.solve(instance,
                           tee = conf['tee'])
    logging.info("Model solved. Solver: %s, Time: %.2f, Gap: %s" %
                     (results.solver.termination_condition, results.solver.time, results.solution(0).gap))
        instance.solutions.load_from(results)
        
    return instance, results.solver, results.solution

















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

# Change the 
path = 'C:/Users/Asun/Github/Pyomo_Playground/Economic_Dispatch'
os.chdir(path)

#Load the model

from model import model

solver = SolverFactory("cplex")

path_instance = "/".join([path,"data.dat"])
instance = model.create_instance(path_instance)

instance.pprint()

results = opt.solve(instance,
                    tee = True)

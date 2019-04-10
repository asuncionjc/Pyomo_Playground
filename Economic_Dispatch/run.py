# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:59:09 2019

@author: Asun
"""

from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Este paquete te sirve para cambiar directorio
import os

# Ruta carpeta donde estás trabajando
path = 'C:/Users/Asun/Github/Pyomo_Playground/Economic_Dispatch'
os.chdir(path)

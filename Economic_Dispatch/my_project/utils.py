# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 15:45:05 2019

@author: Asun
"""

import logging
import yaml

## Preprocessing

def read_yaml(filename):
    """ Loads YAML file to dictionary"""
    with open(filename, 'r') as f:
        try:
            return yaml.load(f)
        except yaml.YAMLError as exc:
            logging.error('Cannot parse config file: {}'.format(filename))
            raise
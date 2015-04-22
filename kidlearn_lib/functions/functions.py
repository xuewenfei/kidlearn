#-*- coding: utf-8 -*-
#from ssb import *
import re
import pickle
import json
import copy
import os
import sys 
import numpy as np
import scipy
import math

###############################################################################
# Math functions 
###############################################################################

def logistic_function(x,eta = 10,alpha = 0.6):
    y = 1.0/(1+math.exp(-eta*(x-alpha)))
    return y

###############################################################################
# JSON functions 
###############################################################################

def j_str_type(data):
    
    str_data = "\"%s\"" % str(data)
    return str_data

def j_couple(key,value,value_is_string):
    
    key = j_str_type(key)
    
    if value_is_string :
        value = j_str_type(value)        
    
    str_json = "%s: %s" % (key,str(value))
    return str_json

def j_col(data1,data2):
    
    str_json = "%s, %s" % (data1,data2)
    
    return str_json

def j_finish(str_json):
    
    str_json = "{%s}" % str_json
    return str_json
    
def j_col_many(datas):
    
    size = len(datas)
    str_json = datas[0]
    for i in range(1,size):
        str_json = j_col(str_json,datas[i])
    
    str_json = j_finish(str_json)
    
    return str_json

###############################################################################
# Files gestion functions 
###############################################################################

def generatePaths(directory = "HSSBG_TEST1",main_directory = "Simulation/",type_data = "/data_simu_"):
    path_dir = main_directory + directory
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
        
    path_data = path_dir + type_data + directory + ".txt" 
    if path_dir[-1] != "/":
        path_dir += "/" + directory + "_"

    return path_dir,path_data

def write_in_file(path,stringToWrite, optionWrite = "w"):
    with open(path,optionWrite) as fp:
        fp.write(stringToWrite)

    return


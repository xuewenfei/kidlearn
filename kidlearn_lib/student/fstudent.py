#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Fstudentstudent
# Purpose:
#
# Author:      Bclement
#
# Created:     14-03-2015
# Copyright:   (c) BClement 2015
# Licence:     GNU Affero General Public License v3.0

#------------------------------------

from .student import Student
from .. import functions as func
import numpy as np


################################################################################
# Class KT with feature student
################################################################################

class Fstudent(Student):

    def __init__(self, params=None, f=None):
        Student.__init__(self, params=params)
        features = [[2, 0, 0, 0],
                    [0, 2, 0, 0],
                    [0, 0, 2, 0],
                    [0, 0, 0, 2]
                    ]

        #[[0, 0, 0, 0],
        # [1, 1, 1, 1],
        # [2, 2, 2, 2],
        # [3, 3, 3, 3]
        # ]

        f = f  # or np.random.randint(0, len(features))
        self.f_num = f

        self.features = features[f]

    def answer(self, act):
        if act == str(self.f_num):
            reward = [1, 4]
        else:
            reward = [0, 0]
        return reward

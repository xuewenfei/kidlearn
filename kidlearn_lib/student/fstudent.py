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

    def __init__(self, params=None, f=None, features=None):
        Student.__init__(self, params=params)
        # if features == None:
        #     features = [[1, 0, 0, 0],
        #                 [0, 1, 0, 0],
        #                 [0, 0, 1, 0],
        #                 [0, 0, 0, 1]
        #                 ]

        # [[0, 0, 0, 0],
        # [1, 1, 1, 1],
        # [2, 2, 2, 2],
        # [3, 3, 3, 3]
        # ]

        self.f_num = f # or np.random.randint(0, len(features))

        self.features = features

    def answer(self, act, act_feat=None):
        if act_feat is None:
            return self.answer_basic(act)

        prob_correct = self.compute_prob_correct_answer(act_feat)
        s = np.random.multinomial(1, [1 - prob_correct, prob_correct])
        ans = np.nonzero(s == 1)[0][0]

        return ans

    def compute_prob_correct_answer(self, act_feat):
        if len(act_feat) < len(self.features):
            diff = np.diff(np.array([self.features[0:len(act_feat)], act_feat]), axis=0)
        else:
            diff = np.diff(np.array([self.features, act_feat[0:len(self.features)]]), axis=0)
        sum_diff = np.sum(abs(diff))
        
        prob_correct = 1 / (pow(1 + sum_diff,1))

        return prob_correct

    def answer_basic(self, act):
        act = int(act)

        if act == self.f_num:
            reward = 1 # [1, 4]
        else:
            reward = 0# [0, 0]
        return reward

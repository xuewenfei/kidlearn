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

    def __init__(self, params=None, f=None, features=None, profile=None):
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
        self.profile = profile
        if type(f) != int and profile is None:
            self.f_num = f
            self.profile = list(num_f)
        else:
            self.f_num = f  # or np.random.randint(0, len(features))
        self.features = features

    def answer(self, act, act_feat=None, return_rNum=False):
        if self.profile is not None:
            return self.answer_joseph_mail_setup(act, return_rNum)
        elif act_feat is None:
            return self.answer_basic(act, return_rNum)
        prob_correct = self.compute_prob_correct_answer(act_feat)
        ans = self.prob(prob_correct)

        return ans

    def compute_prob_correct_answer(self, act_feat):
        if len(act_feat) < len(self.features):
            diff = np.diff(np.array([self.features[0:len(act_feat)], act_feat]), axis=0)
        else:
            diff = np.diff(np.array([self.features, act_feat[0:len(self.features)]]), axis=0)
        sum_diff = np.sum(abs(diff))

        prob_correct = 1 / (pow(1 + sum_diff, 1))

        return prob_correct

    def answer_basic(self, act, return_rNum=False):
        act = int(act[0])

        if act == self.f_num:
            reward = 30  # [1, 4]
            rNum = 3
        elif abs(act - self.f_num) == 1:
            reward = 15
            rNum = 2
        elif abs(act - self.f_num) == 2:
            reward = 0.5
            rNum = 1
        else:
            reward = -20  # [0, 0]
            rNum = 0
        if return_rNum is True:
            return rNum
        return reward

    def answer_joseph_mail_setup(self, act, return_rNum=False):
        int_act = [int(a) for a in act]
        dist_act_prof = np.count_nonzero(np.array(int_act) - np.array(self.profile))

        if dist_act_prof == 0:
            reward = 30  # [1, 4]
            reward = 50  # [1, 4]
            rNum = 3
        elif dist_act_prof == 1:
            reward = 15
            reward = 35
            rNum = 2
        elif dist_act_prof == 2:
            reward = 0.5
            reward = 20.5
            rNum = 1
        else:
            # reward = -20  # [0, 0]
            reward = 0  # [0, 0]
            rNum = 0
        if return_rNum is True:
            return rNum
        return reward


class MailFstudent(Fstudent):
    def __init__(self, params=None, f=None, features=None, profile=None, probabilities=None):
        Fstudent.__init__(self, params=params, f=f, features=features, profile=profile)
        self.probabilities = probabilities


    def anwer(self, act, num_act):
        prob = self.probs[num_act][int(act)]
        if type(prob) is list:
            ans = func.dissample(prob)
        else:
            ans = self.prob_ans(prob)

        return ans
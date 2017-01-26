# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Name:        LINUCB_disjoint
# Purpose:     Linear UCB with disjoin Linear Models from A Contextual-Bandit Approach to Personalized News Article Recommendation
#
# Author:      Bclement
#
# Created:     14-03-2015
# Copyright:   (c) BClement 2015
# Licence:     GNU Affero General Public License v3.0
# -------------------------------------------------------------------------

import numpy as np
import math
from scipy import linalg
import copy
from sklearn.linear_model import LinearRegression

from .. import functions as func

# lin UCB


class LinUCB(object):
    def __init__(self, student_fea_dim=4, all_features=None, actions=None):
        # upper bound coefficient
        self.all_features = all_features
        self.alpha = 3  # if worse -> 2.9, 2.8 1 + np.sqrt(np.log(2/delta)/2)
        self.r1 = 0.5  # if worse -> 0.7, 0.8
        self.r0 = -20  # if worse, -19, -21
        # dimension of user features = d
        self.d = student_fea_dim
        # Aa : collection of matrix to compute disjoint part for each action a, d*d
        self.Aa = {}
        # AaI : store the inverse of all Aa matrix
        self.AaI = {}
        # ba : collection of vectors to compute disjoin part, d*1
        self.ba = {}
        self.r_hist = {}
        self.c_hist = {}
        self.pred = {}

        self.a_max = 0

        self.theta = {}
        self.x = None
        self.xT = None

        if actions is not None:
            self.set_actions(actions, self.d)
        # linUCB

    def set_actions(self, act, dim_feat=4):
        self.act = act
        # init collection of matrix/vector Aa, Ba, ba
        for key in act:
            self.Aa[key] = np.identity(self.d)
            self.ba[key] = np.zeros((self.d, 1))
            self.AaI[key] = np.identity(self.d)
            self.theta[key] = np.zeros((self.d, 1))
            self.c_hist[key] = []
            self.r_hist[key] = []
            # self.pred[key] = LinearRegression(fit_intercept=True)
            # self.pred[key].fit([[0] * dim_feat], [0])

    def update(self, reward):
        # self.c_hist[self.a_max].append(self.xT[0])
        # self.r_hist[self.a_max].append(reward)
        # r = LinearRegression(fit_intercept=False)
        # r.fit(self.c_hist[self.a_max], self.r_hist[self.a_max])
        # self.pred[self.a_max] = r

        # if reward == -1:
        #     pass
        # elif reward == 1 or reward == 0:
        # if reward == 1:
        #     r = self.r1
        # else:
        #     r = self.r0
        r = reward
        self.Aa[self.a_max] += self.x.dot(self.xT)
        self.ba[self.a_max] += r * self.x
        # self.AaI[self.a_max] = linalg.solve(self.Aa[self.a_max], np.identity(self.d))
        self.AaI[self.a_max] = linalg.inv(self.Aa[self.a_max])
        self.theta[self.a_max] = self.AaI[self.a_max].dot(self.ba[self.a_max])
        # else:
        #     # error
        #     pass

    def sample(self, timestamp, user_feat, actions, act_feat=None):
        # xaT = np.array([user_feat])
        # xa = np.transpose(xaT)
        # art_max = -1
        # old_pa = 0
        pa = []
        for action in actions:
            xaT = np.array([user_feat])
            xa = np.transpose(xaT)
            # print self.pred[action].predict([user_feat])
            # pa.append(float(np.array(self.pred[action].predict([user_feat])) + self.alpha * np.sqrt(np.dot(xaT.dot(self.AaI[action]), xa))))
            # print pa
            pa.append(float(np.dot(xaT, self.theta[action]) + self.alpha * np.sqrt(np.dot(xaT.dot(self.AaI[action]), xa))))
        pa = np.array(pa)
        # self.a_max = actions[divmod(pa.argmax(), pa.shape[0])[1]]
        # print pa
        tmp_pa = copy.deepcopy(pa)
        # print func.softmax(tmp_pa)
        tmp_pa = np.array(func.softmax(tmp_pa))
        # print tmp_pa

        # tmp = np.array([x - min(pa) + 0.001 for x in tmp_pa])
        # print tmp
        tmp = tmp_pa / sum(tmp_pa)
        # print tmp
        # print tmp
        self.a_max = actions[func.dissample(tmp)]
        # raw_input()

        # for action in actions:
        #     # x : feature of current action, d*1
        #     # theta = self.AaI[action].dot(self.ba[action])
        #     sa = np.dot(xaT.dot(self.AaI[action]), xa)
        #     new_pa = float(np.dot(xaT, self.theta[action]) + self.alpha * np.sqrt(np.dot(xaT.dot(self.AaI[action]), xa)))
        #     if art_max == -1:
        #         old_pa = new_pa
        #         art_max = action
        #     else:
        #         if old_pa < new_pa:
        #             art_max = action
        #             old_pa = new_pa

        self.x = xa
        self.xT = xaT
        # action index with largest UCB
        # self.a_max = art_max # divmod(pa.argmax(), pa.shape[0])[1]

        return self.a_max

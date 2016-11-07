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

from .. import functions as func

# lin UCB


class LinUCB(object):
    def __init__(self):
        # upper bound coefficient
        self.alpha = 3  # if worse -> 2.9, 2.8 1 + np.sqrt(np.log(2/delta)/2)
        self.r1 = 0.5  # if worse -> 0.7, 0.8
        self.r0 = -20  # if worse, -19, -21
        # dimension of user features = d
        self.d = 4
        # Aa : collection of matrix to compute disjoint part for each article a, d*d
        self.Aa = {}
        # AaI : store the inverse of all Aa matrix
        self.AaI = {}
        # ba : collection of vectors to compute disjoin part, d*1
        self.ba = {}

        self.a_max = 0

        self.theta = {}
        self.x = None
        self.xT = None
        # linUCB

    def set_articles(self, art):
        # init collection of matrix/vector Aa, Ba, ba
        for key in art:
            self.Aa[key] = np.identity(self.d)
            self.ba[key] = np.zeros((self.d, 1))
            self.AaI[key] = np.identity(self.d)
            self.theta[key] = np.zeros((self.d, 1))

    def update(self, reward):
        if reward == -1:
            pass
        elif reward == 1 or reward == 0:
            if reward == 1:
                r = self.r1
            else:
                r = self.r0
            self.Aa[self.a_max] += self.x.dot(self.xT)
            self.ba[self.a_max] += r * self.x
            self.AaI[self.a_max] = linalg.solve(self.Aa[self.a_max], np.identity(self.d))
            self.theta[self.a_max] = self.AaI[self.a_max].dot(self.ba[self.a_max])
        else:
            # error
            pass

    def sample(self, timestamp, context, articles):
        xaT = np.array([context])
        xa = np.transpose(xaT)
        #art_max = -1
        #old_pa = 0
        pa = np.array([float(np.dot(xaT, self.theta[article]) + self.alpha * np.sqrt(np.dot(xaT.dot(self.AaI[article]), xa))) for article in articles])
        self.a_max = articles[divmod(pa.argmax(), pa.shape[0])[1]]
        '''
        for article in articles:
            # x : feature of current article, d*1
            # theta = self.AaI[article].dot(self.ba[article])
            sa = np.dot(xaT.dot(self.AaI[article]), xa)
            new_pa = float(np.dot(xaT, self.theta[article]) + self.alpha * np.sqrt(np.dot(xaT.dot(self.AaI[article]), xa)))
            if art_max == -1:
                old_pa = new_pa
                art_max = article
            else:
                if old_pa < new_pa:
                    art_max = article
                    old_pa = new_pa
        '''
        self.x = xa
        self.xT = xaT
        # article index with largest UCB
        # self.a_max = art_max # divmod(pa.argmax(), pa.shape[0])[1]

        return self.a_max

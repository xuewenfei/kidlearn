#-*- coding: utf-8 -*-
## Zone of Proximal Development and Empirical Success
## 2014 BCLEMENT

from riarit import *

#########################################################
#########################################################
## class ZPDES_hssbg

class ZPDES_hssbg(RIARIT_hssbg):

    def instantiate_ssbg(self,RT):
        return ZPDES_ssbg(RT,self.levelupdate,self.filter1,self.filter2,self.uniformval,algo = "ZPDES")

    def update(self, act, corsol = True, error_ID = None, *args):
        #if act is None:
        #    act = self.lastAct
        #self.computelvl(act)

        answer_impact = self.return_answer_impact(corsol,error_ID)

        for nameRT in act.keys():
            #if self.SSBGs[nameRT].sonSSBG > 0:
            #    print self.SSBGs[nameRT].sonSSBG
            #    print self.SSBGs[nameRT].using_RT[0]
            #    answer_impact = [i + act[self.SSBGs[nameRT].using_RT[0][act[nameRT][0]]][0] for i in answer_impact]
            self.SSBGs[nameRT].update(self.current_lvl_ex[nameRT],act[nameRT], corsol, answer_impact,act)
        return

## class RIARIT_hssbg
#########################################################

#########################################################
#########################################################
## class ZPDES_ssbg
class ZPDES_ssbg(RIARIT_ssbg):

    def instanciate_ssb(self,ii,is_hierarchical,stepUpdate = 8):
        return ZPDES_ssb(ii,len(self.RT[ii]),self.ncompetences,self.requer[ii], self.stop[ii],self.filter1,self.filter2,self.uniformval, algo = self.algo,is_hierarchical = is_hierarchical, using_RT = self.using_RT[ii],step_Update = stepUpdate)

    def calcul_reward(self,act,answer_impact):
        coeff_ans = mean(answer_impact)
        r_ES = []
        for ii in range(self.nactions):
            r_ES.append(self.SSB[ii].calcul_reward_ssb(act[ii],coeff_ans))
        return r_ES

    def update(self,lvl,act,corsol,answer_impact,*args, **kwargs):
        r_ES = self.calcul_reward(act,answer_impact)
        
        ## For simulation
        r_KC = RIARIT_ssbg.calcul_reward(self,lvl,corsol,answer_impact)
        ## for simulation

        for ii in range(self.nactions):
            self.nbturn[ii] += 1
            #if len(self.SSB[ii].sonSSBG.keys()) > 0:
            #    r_ES[ii] += pow(10,-5)*all_act[self.using_RT[ii][act[ii]]][0]/len(self.SSB[ii].sonSSBG[self.using_RT[ii][act[ii]]].SSB[0].bandval)
                #raw_input()
            self.SSB[ii].update(act[ii], max(0,r_ES[ii]))
            self.SSB[ii].promote()

## class ZPDES_ssbg
#########################################################

#########################################################
#########################################################
## class ZPDES_ssb

class ZPDES_ssb(RIARIT_ssb):

    def __init__(self,id, nval, ntask, requer, stop, filter1,filter2,uniformval, algo = "ZPDES",is_hierarchical = 0, using_RT = [],step_Update = 8):

        with open('data.json', 'rb') as fp:
            ssb_data = json.load(fp)

        SSbandit.__init__(self,id, nval, ntask, filter1,filter2,uniformval, algo,is_hierarchical,using_RT)
        self.stepUpdate = ssb_data['stepUpdate']
        self.size_window = min(len(self.bandval),ssb_data['size_window'])
        self.promote(True)

    def hierarchical_promote(self):
        for i in range(1,self.nval):
            if(self.bandval[i]== 0):
                try:
                    ssbg = self.sonSSBG[self.using_RT[i-1]]
                except:
                    print "son : %s, i : %s, lenact : %s, uRT : %s" % (self.sonSSBG,i,self.nval,self.using_RT) 
                    crash()
                successUsed = []
                sumSucess = 0
                for ssb in ssbg.SSB:
                    if ssb.is_hierarchical == 1:
                        for suc in ssb.success:
                            if suc == []:
                                sucToTreat = [0]
                            else:
                                sucToTreat = suc
                            stepMax = self.stepUpdate/2
                            stepSuccess = min(len(sucToTreat),stepMax) 
                            successUsed.append(sucToTreat[-stepSuccess:])
                            sumSucess += mean(sucToTreat[-stepSuccess:])

                meanSucess = sumSucess*1.0/max(len(successUsed),1)
                thresZProm = 1.0/3 #len(ssbg.SSB)/4

                if meanSucess > thresZProm:
                    self.bandval[i] = self.bandval[i-1]/4 #TODO test with 4 for exemple

    def promote(self,init = False):
        stepMax = self.stepUpdate/2
        stepSuccess = min(len(self.success),stepMax)
        #if "mod" in self.using_RT :#and self.algo == "ZPDES":
        #    print "YOLO"
        #print self.using_RT
        #print self.sonSSBG
        #raw_input()
        if init == True :
            for ii in range((1-self.is_hierarchical)*(len(self.bandval)-1)+1):
                self.bandval[ii] = self.uniformval#/pow((ii+1),7)
        elif len(self.sonSSBG) > 0:
            self.hierarchical_promote()
        elif len(self.bandval) - self.bandval.count(0) < self.size_window and self.bandval[0] != 0:
            for i in range(1,len(self.bandval)- self.bandval.count(0)+1):
                if mean(self.success[i-1][-stepSuccess:]) > 0.5  and len(self.success[i-1]) > 1 and self.bandval[i:] == [0]*len(self.bandval[i:]):
                    self.bandval[i] = self.bandval[i-1]
        else :
            first = -1
            for ii in range(self.nval):
                if self.bandval[ii] != 0:
                    first = ii
                    break
            for ii in range(self.nval):
                if self.bandval[ii] != 0:
                    last = ii

            valToUp = 1.0/2
            #last = first + 2
            #if first == len(self.bandval) - 3:
            #    valToUp = (1.0*stepSuccess/2 + 1)/stepSuccess
            #elif first == len(self.bandval) - 2:
            #  #  last = first+1
            #    valToUp = (1.0*stepSuccess/2 + 1)/stepSuccess
            #valToUp = 0.6
            if first >= len(self.bandval) - 3:
                valToUp = 0.5
            elif len(self.bandval) <= 3:
                valToUp = 0.5
            else:
                last = first

            if mean(self.success[first][-stepSuccess:]) > valToUp and len(self.success[last]) >= stepMax and first < len(self.bandval) - 3: 
                self.bandval[first] = 0

                if first+3 < len(self.bandval):
                    self.bandval[first+3] = min(self.bandval[first+2],self.bandval[first+1])/2

        return

    def calcul_reward_ssb(self,val,coeff_ans):
        self.success[val].append(coeff_ans)
        #if len(self.sonSSBG.keys())> 0:
        #    print self.success
        if len(self.success[val]) > 1 :
            y_step = min(self.stepUpdate,len(self.success[val]))
            y_range = y_step/2
            sum_old = mean(self.success[val][-y_step:-y_range])
            sum_range = mean(self.success[val][-y_range:])
            r = max(0,sum_range - sum_old)

        elif len(self.success[val]) == 1:
            r = 0.5
        else:
            r = 1

        return r


## class ZPDES_ssb
#########################################################
#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        experimentation
# Purpose:
#
# Author:      Bclement
#
# Created:     14-03-2015
# Copyright:   (c) BClement 2015
# Licence:     GNU Affero General Public License v3.0
#-------------------------------------------------------------------------------

import os
import sys
import copy
import json
import numpy as np
import uuid
import time

# from ..seq_manager import Sequence, ZpdesHssbg, RiaritHssbg, RandomSequence, POMDP
from ..exercise import Exercise
from ..student import Population
from ..config import datafile
from .. import config
from .. import functions as func
from experimentation import SessionStep, WorkingSession, WorkingGroup
#import config.datafile as datafile

#########################################################
#########################################################
# class SessionStep

class OsOaSS(SessionStep):

    """\
        SessionStep Definition
    """

    def __init__(self, student_state=None, seq_manager_state=None, exercise=None, *args, **kwargs):
        if student_state is None:
            student_state = {}
        if seq_manager_state is None:
            seq_manager_state = {}

        self.student = student_state
        self.seq_manager = seq_manager_state
        if exercise is not None:
            self.exercise = exercise.state
        else:
            self.exercise = exercise

        for key, val in kwargs.iteritems():
            object.__setattr__(self, key, val)

    @property
    def act(self):
        return self.exercise["act"]

    @property
    def answer(self):
        return self.exercise["answer"]

    def __repr__(self):
        return "act : {}, student skill: {}".format(self.exercise, self.student["knowledges"])

    ###########################################################################
    # Data Analysis tools
    def get_attr(self, attr, *arg, **kwargs):
        data = getattr(self, attr)
        if len(arg) > 0:
            if isinstance(data, dict):
                return data[arg[0]]
            else:
                data = getattr(data, arg[0])
        return data

    def base(self):
        return

    # Data Analysis tools
    ###########################################################################

# class SessionStep
#########################################################

#########################################################
#########################################################
# class WorkingSession

class OsOaWS(WorkingSession):

    def __init__(self, params=None, params_file=None, directory="params_files", student=None, seq_manager=None, *args, **kwargs):

        if params is not None or params_file is not None:
            params = params or func.load_json(params_file, directory)
        self.params = params

        self._student = student or config.student(self.params["student"])
        self.uuid = self._student.uuid
        self._seq_manager = seq_manager or config.seq_manager(self.params["seq_manager"])

        self._KC = self._student.KC_names

        self._step = []
        self._current_ex = None
        self.save_actual_step()
        #self.log = SessionLog

    @property
    def student(self):
        return self._student

    @property
    def step(self):
        return self._step

    @property
    def nb_step(self):
        return len(self._step)

    @property
    def seq_manager(self):
        return self._seq_manager

    @property
    def main_act(self):
        return self._seq_manager.main_act

    @property
    def KC(self):
        return self._KC

    # methods

    def run(self, nb_ex):
        for i in range(nb_ex):
            self.step_forward()
        self.free_data()

    def step_forward(self):
        ex = self.new_exercise()
        self.student_answer(ex)
        self.save_actual_step(ex)
        #self.log.log(new_ex, student_answer)
        self.update_manager(ex)

    def new_exercise(self):
        act = self._seq_manager.sample()
        ex_skill_lvl = self._seq_manager.compute_act_lvl(act, "main")  # ,dict_form =1)
        self._current_ex = Exercise(act, ex_skill_lvl, self._KC)
        return self._current_ex

    def student_answer(self, ex, answer=None, nb_try=0):
        if answer:
            self._student.answer(ex, answer, nb_try=nb_try)
        else:
            self._student.answer(ex, nb_try=nb_try)

    def update_manager(self, ex):
        self._seq_manager.update(ex.act, ex._answer)

    def actual_step(self, ex=None):
        return SessionStep(copy.deepcopy(self._student.get_state()), copy.deepcopy(self._seq_manager.get_state()), copy.deepcopy(ex or self._current_ex))

    def save_actual_step(self, ex=None):
        self._step.append(self.actual_step(ex))

    def free_data(self):
        self._student = None
        #self._seq_manager = None

    def compute_all_act_level(self, data, model="KT"):
        if model == "KT":
            pass
        elif model == "":
            pass
        return

    ###########################################################################
    # Data Analysis tools

    def calcul_cost(self, begin=1, time=None, gamma=0.99):
        if time is None:
            time = len(self._step)
        return sum([pow(gamma, t) * sum(self.student_level_time(time=t, kc=range(len(self._KC)))) for t in range(begin, time)])

    def time_max_level(self):
        level_all_time = [sum(self.student_level_time(time=t, kc=range(len(self._KC)))) for t in range(len(self._step))]
        return np.argmax(level_all_time)

    def student_level_time(self, time=0, kc=0):
        if isinstance(kc, list):
            # return [self._step[time].student["knowledges"][k].level for k in kc]
            return self._step[time].student["knowledges"]

        elif kc >= len(self._step[time].student["knowledges"]):
            return np.mean(self._step[time].student["knowledges"])
            # return np.mean([self._step[time].student["knowledges"][k].level for k in range(len(self._step[time].student["knowledges"]))])
        else:
            return self._step[time].student["knowledges"][kc]  # .level

    def get_act_obs(self, begin_time=1, end_time=None, act_key="KT6kc", **kwargs):
        act = []
        obs = []
        for step in self._step[begin_time:end_time]:
            act.append(step.act[act_key][0])
            obs.append(step.answer)

        return np.array([act, obs])

    def base(self):
        return

    # Data Analysis tools
    ###########################################################################

# class WorkingSession
#########################################################

#########################################################
#########################################################
# class WorkingGroup
class OsOaWG(WorkingGroup):

    def __init__(self, params=None, params_file=None, directory="params_files", population=None, WorkingSessions=None, *args, **kwargs):
        # params :
        if params is not None or params_file is not None:
            params = params or func.load_json(params_file, directory)
        else:
            params = {}
        self.params = params
        self.logs = {}
        self.uuid = str(uuid.uuid1())

        if WorkingSessions:
            self._working_sessions = WorkingSessions

        else:
            population = population or config.population(params=params["population"])
            if type(population) == Population:
                population = population.students

            self._working_sessions = []
            for student_params in population:
                params = {"student": student_params, "seq_manager": self.params["seq_manager"]}
                self._working_sessions.append(WorkingSession(params=params))

    @property
    def KC(self):
        return self._working_sessions[0].KC

    @property
    def main_act(self):
        return self._working_sessions[0].main_act

    @property
    def working_sessions(self):
        return self._working_sessions

    @property
    def students(self):
        students = [ws.student for ws in self._working_sessions]
        return students

    def get_WorkingSession(self, num_stud=0, id_stud=None):
        if id_stud:
            for ws in self._working_sessions:
                if ws.student.id == id_stud:
                    return ws

        return self._working_sessions[num_stud]

    def step_forward(self):
        for ws in self._working_sessions:
            ws.step_forward()

    def run(self, nb_ex):
        for ws in self._working_sessions:
            ws.run(nb_ex)

    def add_student(self, student, seq_manager):
        self._working_sessions.append(WorkingSession(student, seq_manager))

    ###########################################################################
    # Data Analysis tools

    def calcul_cost(self):
        cost = []
        for ws in self._working_sessions:
            cost.append(ws.calcul_cost())
        return cost

    def get_students_level(self, time=0, kc=0):
        skill_level = []
        for ws in self._working_sessions:
            skill_level.append(ws.student_level_time(time, kc))
        return skill_level

    def get_data_time(self, time=0, attr=None, *arg, **kwargs):
        data = []
        for ws in self._working_sessions:
            if attr:
                data.append(ws.step[time].get_attr(attr, *arg))
            else:
                data.append(ws.step[time])
        return data

    def get_act_repartition_time(self, first_ex=1, nb_ex=101, act="MAIN", nb_act=5):
        repart = [[0 for x in range(nb_act)]]
        for num_ex in range(first_ex, nb_ex):
            exs = self.get_data_time(num_ex, "exercise", "act")
            for j in range(len(exs)):
                repart[exs[j][act][0]][num_ex - first_ex][0] += 1

        return repart

    def get_ex_repartition_time(self, first_ex=1, nb_ex=101, type_ex=["M", "R", "MM", "RM"],
                                nb_ex_type=[6, 4, 4, 4], main_rt="MAIN"):

        repart = [[] for x in range(len(type_ex))]
        for num_ex in range(first_ex, nb_ex):
            exs = self.get_data_time(num_ex, "exercise", "act")
            for nbType in range(len(type_ex)):
                repart[nbType].append([0 for i in range(nb_ex_type[nbType])])
                # print repart
            for j in range(len(exs)):
                if nb_ex_type[exs[j][main_rt][0]] == 1:
                    repart[exs[j][main_rt][0]][num_ex - first_ex][0] += 1
                else:
                    repart[exs[j][main_rt][0]][num_ex - first_ex][exs[j][type_ex[exs[j][main_rt][0]]][0]] += 1

        return repart

    def get_act_obs(self, begin_time=1, end_time=None, **kwargs):
        act_obs = []
        for ws in self.working_sessions:
            act_obs.append(ws.get_act_obs(begin_time, end_time, **kwargs))
        return act_obs

    # Data Analysis tools
    ###########################################################################


# class WorkingGroup
#########################################################
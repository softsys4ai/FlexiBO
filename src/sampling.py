#! /usr/bin/env python2.7
from __future__ import division
from pareto import Pareto
import numpy as np
import random
import copy


class Sampling(object):
    """This class is used to determine next sample and objective
    Attributes:
    NUM_OBJ: number of objectives
    O1_COST: cost of evalauting objective O1
    O2_COST: cost of evalauting objective O2
    """
    def __init__(self):
         print "[STATUS]: initializing sampling class"
         self.O1_IND = 1
         self.O2_IND = 0
         self.NUM_OBJ = 2
         self.O1_COST = 1
         self.O2_COST = 8.8 * self.O1_COST
         self.objectives = ["o2", "o1"]
         self.pareto = Pareto()

    def monte_carlo_sampling(
                             self,
                             min_x,
                             max_x):

        """This function is used for monte carlo sampling"""

        val = [random.uniform(min_x, max_x) for i in xrange(10)]
        return np.mean(val)

    def compute_max_dv_per_cost(self):
        """This function is used to compute max dv per cost"""
        max_dv_per_cost=0
        selected_objective = "o1"
        selected_index = 0
        for index in self.dv_per_cost:
            for obj in self.objectives:
                if self.dv_per_cost[index][obj] > max_dv_per_cost:
                    max_dv_per_cost = self.dv_per_cost[index][obj]
                    selected_objective = obj
                    selected_index = index

        return (
                selected_index,
                selected_objective)

    def determine_next_sample(

                             self,
                             undom_indices,
                             pareto_volume,
                             REGION,
                             E,
                             O):

        """This function is used to determine next sample"""
        selected_sample_ind = None
        selected_sample = None
        selected_objective = None

        self.dv_per_cost={}
        for ui in undom_indices:
            self.dv_per_cost[ui]={"o1":0, "o2":0}

        for index in undom_indices:
            for obj in self.objectives:
                cur_region = copy.deepcopy(REGION)
                if O[index][obj] is False:
                    ondex = self.objectives.index(obj)
                    # shrink value to expected average using monte carlo
                    cur_min = cur_region[index]["pes"][ondex]
                    cur_max = cur_region[index]["opt"][ondex]
                    shrunk_val = self.monte_carlo_sampling(cur_min, cur_max)
                    # update to shrunk value
                    cur_region[index]["pes"][ondex] = shrunk_val
                    cur_region[index]["opt"][ondex] = shrunk_val
                    # identify updated undominated points
                    (cur_undom_ind,
                    cur_undom) = self.pareto.identify_undom_points(cur_region)
                    # construct updated pessimistic front
                    cur_pes_pareto = self.pareto.construct_pes_pareto_front(
                                               cur_undom_ind,
                                               cur_undom)
                    # construct updated pessimistic front
                    cur_opt_pareto = self.pareto.construct_opt_pareto_front(
                                                cur_undom_ind,
                                                cur_undom)
                    # compute updated pes volume
                    cur_pes_volume = self.pareto.compute_pareto_volume(cur_pes_pareto)
                    # compute updated opt volume
                    cur_opt_volume = self.pareto.compute_pareto_volume(cur_opt_pareto)
                    # compute cur pareto volume
                    cur_pareto_volume = cur_opt_volume - cur_pes_volume
                    # compute dv
                    dv = pareto_volume - cur_pareto_volume

                    if obj == "o1":
                        self.dv_per_cost[index][obj] = dv/self.O1_COST
                    elif obj == "o2":
                        self.dv_per_cost[index][obj] = dv/self.O2_COST
                    else:
                        print "invalid objective"


        (selected_sample_ind,
        selected_objective)=self.compute_max_dv_per_cost()
        selected_sample = copy.deepcopy(E[selected_sample_ind])

        return (
                selected_sample_ind,
                selected_sample,
                selected_objective)

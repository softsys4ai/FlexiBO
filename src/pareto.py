#! /usr/bin/env python2.7
import numpy as np
from operator import itemgetter

class Pareto(object):
    def __init__(self):
        print " [STATUS]: initializing pareto class"
        self.O1_IND = 1
        self.O2_IND = 0

    def compute_pareto_volume(self,
                              front):
        """This function is used to compute pareto volume between pessimistic and
        optimistic pareto front
        """

        prev_x = 0
        prev_y = 0
        area = 0
        for point in front:
            a = point[self.O1_IND]
            b = point[self.O2_IND] - prev_x
            area += a*b
            prev_x = point[self.O2_IND]

        return area


    def construct_pes_pareto_front(
                                   self,
                                   pareto_points_ind,
                                   pareto_points):
        """This function is used to construct pessimistic pareto front using the
        undom points
        """

        pess_pareto = list()
        indices_map = {}
        for point in xrange(len(pareto_points)):
            indices_map[point] = pareto_points_ind[point]
            pess_pareto.append(pareto_points[point]["pes"])

        # sort along object1 in descending order
        sorted_pess_ind = sorted(range(len(pess_pareto)),
                        key = lambda k: pess_pareto[k][self.O1_IND])[::-1]

        #-----------------------------------------------------------------------
        # pessimistic Pareto Front Computation
        #-----------------------------------------------------------------------
        pess_o2 = [pess_pareto[i][self.O2_IND] for i in sorted_pess_ind]
        i = 0
        max_val = []
        orig = []
        sampled_pess_pareto_ind = []
        while i < len(pess_o2):
            cur = pess_o2[i]
            sampled_pess_pareto_ind.append(i)
            orig.append(i)

            for j in xrange(i+1, len(pess_o2)):
                if cur >= pess_o2[j]:
                    sampled_pess_pareto_ind.append(i)
                    max_val.append(j)
                    orig.append(j)
            if len(max_val) != 0:
               i = np.max(max_val) + 1
               max_val = []
            else:
               i = i+1
        sampled_pess_pareto = [[pess_o2[sampled_pess_pareto_ind[i]],
                                pess_pareto[i][self.O1_IND]]
                                for i in xrange(len(orig))]
        return sampled_pess_pareto



    def construct_opt_pareto_front(
                                   self,
                                   pareto_points_ind,
                                   pareto_points):
        """This function is used to construct optimistic pareto front using the
        undom points"""

        opt_pareto = list()
        indices_map = {}
        for point in xrange(len(pareto_points)):
            indices_map[point] = pareto_points_ind[point]
            opt_pareto.append(pareto_points[point]["opt"])

        # sort along object1 in descending order
        sorted_opt_ind = sorted(range(len(opt_pareto)),
                       key = lambda k: opt_pareto[k][self.O1_IND])[::-1]
        #-----------------------------------------------------------------------
        # optimistic Pareto Front Computation
        #-----------------------------------------------------------------------
        # sample optimistic pareto points
        cur = opt_pareto[sorted_opt_ind[0]]
        # initialize
        sampled_opt_pareto_ind = [sorted_opt_ind[0]]
        sampled_opt_pareto = [cur]
        for ind in xrange(1, len(sorted_opt_ind)):
            next = opt_pareto[sorted_opt_ind[ind]]
            if next[self.O2_IND] >= cur[self.O2_IND]:
                sampled_opt_pareto_ind.append(sorted_opt_ind[ind])
                sampled_opt_pareto.append(next)
            cur = opt_pareto[sorted_opt_ind[ind]]


        return sampled_opt_pareto


    def identify_undom_points(
                              self,
                              region):
        """This function is used to determine the dom points that will be
        included in the pessimistic and optimistic pareto front.
        """
        dom_points_ind = list()
        pes_pareto, opt_pareto = list(), list()
        undom_points_ind = [i for i in xrange(len(region))]

        for i in undom_points_ind:
            # if the current config is not dom
            if i != -1:
                cur = region[i]
                for j in undom_points_ind :
                    # check only undom configs other than current
                    if (j != i or j !=-1):
                        # check if current config is dom
                        if (region[j]["pes"][self.O1_IND] >= cur["opt"][self.O1_IND] and
                           region[j]["pes"][self.O2_IND] >= cur["opt"][self.O2_IND]):
                           # append the current config to dom
                            dom_points_ind.append(i)
                            undom_points_ind[i] = -1

                        # check if current config dominates
                        if (region[j]["opt"][self.O1_IND] < cur["pes"][self.O1_IND] and
                           region[j]["opt"][self.O2_IND] < cur["pes"][self.O2_IND]):
                           # append the config that is dom by current to dom
                            dom_points_ind.append(j)
                            undom_points_ind[j] = -1

        # TODO: dom points indices multiple occurence issue
        undom_points_ind = [i for i in undom_points_ind if i not in (-1, -1)]
        undom_points = [region[i] for i in undom_points_ind]

        return (
                undom_points_ind,
                undom_points)

    def compute_improvement_per_cost(self):
        """This function is used to compute improvement per cost"""
        print "Improvement/Cost"

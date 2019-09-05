#! /usr/bin/env python2.7
import math
import copy
import config
import numpy as np
from pareto import Pareto
from sampling import Sampling
from modeling import Modeling


class FlexiBO(object):
    """This class is used to implement an active learning approach to optimize
    multiple objectives of different cost
    E: design space

    O: evaluated objectives
    n: number of objectives
    m1: objective 1
    m2: objective 2
    """
    def __init__(self,
                mode):
        print "[STATUS]: initializing flexibo class"
        # define constants
        self.NUM_ITER = 5
        self.NUM_OBJ = 2
        self.O1_IND = 1
        self.O2_IND = 0
        if mode == "Test": self.conf = config.ConfigTest()
        # mode of flexibo operation
        elif mode == "Real": self.conf = config.ConfigReal()
        elif mode == "Synthetic": self.conf = config.ConfigSynthetic()
        else: print "mode not supported" ; return
        # get design space
        (self.E,
        self.O,
        self.measurement) = self.conf.set_design_space()
        self.conf.set_evaluation()
        # define handlers for utils classes
        self.pareto = Pareto()
        self.sampling = Sampling()
        self.SM = Modeling()
        # run bayesian optimization loop
        self.perform_bo_loop()

    def perform_bo_loop(self):
        """This function is used to perform bayesian optimization loop
        U: Design Space
        REGION: Uncertainty Region for each configuration in design space
        """
        # initialization
        BETA = 1.0
        (eval_O1,
        eval_O2,
        init_X,
        init_Y1,
        init_Y2,
        init_measured_indices) = self.conf.set_evaluation()

        for i in xrange(len(init_measured_indices)):
            self.O[i]["o1"] = True
            self.measurement[init_measured_indices[i]]["o1"] = init_Y1[i][0]
            self.O[i]["o2"] = True
            self.measurement[init_measured_indices[i]]["o2"] = init_Y2[i][0]

        init_X = np.array(init_X)
        init_Y1 = np.array(init_Y1)
        init_Y2 = np.array(init_Y2)


        U = np.array(self.E[:])
        init_X1 = copy.deepcopy(init_X)
        init_X2 = copy.deepcopy(init_X)

        # bo loop
        for iteration in xrange(self.NUM_ITER):
            print "---------------------------------------Iteration: ",iteration
            REGION = [{} for _ in U]
            # fit a surrogate model for each objective
            model_o1 = self.SM.fit_gp(
                                      init_X1,
                                      init_Y1)
            model_o2 = self.SM.fit_gp(
                                      init_X2,
                                      init_Y2)
            for config in xrange(len(U)):
                # compute mu and sigma of each points for each objective
                cur = np.array([U[config]])
                cur_eval = self.O[config]

                # objective 1
                if cur_eval["o1"] is False:
                    mu_o1, sigma_o1 = self.SM.get_gp_model_params(
                                              model_o1,
                                              cur)
                else:
                    mu_o1, sigma_o1 = self.measurement[config]["o1"], 0

                # objective 2
                if cur_eval["o2"] is False:
                    mu_o2, sigma_o2 = self.SM.get_gp_model_params(
                                              model_o2,
                                              cur)
                else:
                    mu_o2, sigma_o2 = self.measurement[config]["o2"], 0

                # compute uncertainty region for each point using mu and sigma
                pes_o1=mu_o1 - math.sqrt(BETA) * sigma_o1
                pes_o2=mu_o2 - math.sqrt(BETA) * sigma_o2
                REGION[config]["pes"] = [
                                      0 if (pes_o1 < 0) else pes_o1,
                                      0 if (pes_o2 < 0) else pes_o2]
                REGION[config]["avg"] = [
                                      mu_o1,
                                      mu_o2]
                REGION[config]["opt"] = [
                                      mu_o1 + math.sqrt(BETA) * sigma_o1,
                                      mu_o2 + math.sqrt(BETA) * sigma_o2]

            self.REGION = [
                   {'opt': [2, 11], 'avg': [1, 10], 'pes': [0.5,9]},
                   {'opt': [3, 9], 'avg': [2.5, 8], 'pes': [1.5,7]},
                   {'opt': [1.5, 7], 'avg': [1, 6], 'pes': [0.5,5]},
                   {'opt': [5, 6], 'avg': [4.5, 5], 'pes': [4,4]},
                   {'opt': [7.5, 4], 'avg': [6.5, 3], 'pes': [6,2.5]},
                   {'opt': [3.5, 3.5], 'avg': [3, 3], 'pes': [2.5,2.5]},
                   {'opt': [5.5, 3], 'avg': [5, 2], 'pes': [4.5,1.5]}
                   ]

            # determine undom points
            (undom_points_ind,
            undom_points) = self.pareto.identify_undom_points(self.REGION)

            # determine pes pareto front
            pes_pareto = self.pareto.construct_pes_pareto_front(
                                     undom_points_ind,
                                     undom_points)
            # determine opt pareto front
            opt_pareto = self.pareto.construct_opt_pareto_front(
                                     undom_points_ind,
                                     undom_points)

            # determine pes pareto volume
            pes_pareto_volume = self.pareto.compute_pareto_volume(pes_pareto)
            # determine opt pareto volume
            opt_pareto_volume = self.pareto.compute_pareto_volume(opt_pareto)

            # determine volume of the pareto front
            pareto_volume = opt_pareto_volume - pes_pareto_volume

            # determine next configuration and objective
            (next_X_index,
            next_X,
            next_objective) = self.sampling.determine_next_sample(
                                       undom_points_ind,
                                       pareto_volume,
                                       self.REGION,
                                       self.E,
                                       self.O)

            # perform measurement on next Sampling on the objective returned and
            if next_objective == "o1":
                cur_X1, cur_Y1 = self.conf.get_measurement(eval_O1,
                                                  next_X)
                self.O[next_X_index][next_objective] = True
                self.measurement[next_X_index][next_objective] = cur_Y1[0]
                np.vstack((init_X1, cur_X1))
                np.vstack((init_Y1, cur_Y1))

            elif next_objective == "o2":
                cur_X2, cur_Y2 = self.conf.get_measurement(eval_O2,
                                                  next_X)
                self.O[next_X_index][next_objective] = True
                self.measurement[next_X_index][next_objective] = cur_Y2[0]
                np.vstack((init_X2, cur_X2))
                np.vstack((init_Y2, cur_Y2))

            else:
                print "Invalid objective"

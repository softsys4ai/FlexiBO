#! /usr/bin/env python2.7
import itertools
import pandas as pd

class ConfigTest:
    """This class is used to create configuration space for test cases
    """
    def __init__(self):
        print "[STATUS]: initializing configtest class"

    def set_design_space(self):
        """This function is used to create discrete design space usign bounds
        @output: design space
        """
        bounds=[
                [1],
                [0,1],
                [0,1],
                [0,1],
                [345600, 499200, 652800,
                806400,960000, 1113600,
                1267200, 1420800, 1574400,
                1728000, 1881600, 2035200],
                [140250000, 497250000, 943500000,
                1300500000],
                [1062400000, 1331200000, 1600000000,
                1866000000]
                ]
        permutation = list(itertools.product(*bounds))
        return (
                [list(x) for x in permutation],
                [{"o1":False, "o2":False} for _ in permutation],
                [{"o1":False, "o2":False} for _ in permutation])

    def set_evaluation(self):
        """This function is used to set objective evaluation manager"""
        testdir = "~/FlexiBO/data/Input/it_ec_te_obj.csv"
        df = pd.read_csv(testdir)
        # objective test class
        from objective_test import ObjectiveTest
        m1 = "inference_time"
        m2 = "temperature"
        self.OT = ObjectiveTest()
        (X,
        Y1,
        Y2) = self.OT.prepare_training_data(
                                      df,
                                      m1,
                                      m2)
        (rf1,
        rf2) = self.OT.fit_rf(
                         X,
                         Y1,
                         Y2)

        (init_X,
        init_Y1,
        init_Y2,
        init_index)= self.OT.initialize(
                      X,
                      Y1,
                      Y2)

        return (
                rf1,
                rf2,
                init_X,
                init_Y1,
                init_Y2,
                init_index)

    def get_measurement(self,
                       evaluator,
                       sample):
        """This function is used to get meaurement using evaluator"""
        x, y = self.OT.measurement(evaluator,
                              sample)
        return x, y



class ConfigReal:
    """This class is used to create configuration space for real cases for DNN systems
    """
    def __init__(self):
        print "[STATUS]: initializing configreal class"


class ConfigSynthetic:
    """This class is used to create configuration space for synthetic cases
    """
    def __init__(self):
        print "[STATUS]: initializing configsynthetic class"

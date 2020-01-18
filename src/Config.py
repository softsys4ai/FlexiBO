import itertools
import pandas as pd
import numpy as np

class ConfigTest:
    """This class is used to create configuration space for test cases
    """
    def __init__(self):
        print ("[STATUS]: initializing configtest class")

    def set_design_space(self):
        """This function is used to create discrete design space usign bounds
        @output: design space
        """
        bounds=[
                [1, 2, 3,
                4],
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
        print ("[STATUS]: initializing configreal class")

    def set_design_space(self):
        """This function is used to set design space for real cases"""
        bounds=[
                [1, 2, 3,
                4],
                [345600, 499200, 652800,
                806400,960000, 1113600,
                1267200, 1420800, 1574400,
                1728000, 1881600, 2035200],
                [140250000, 497250000, 943500000,
                1300500000],
                [1062400000, 1331200000, 1600000000,
                1866000000]                                       
                #[0, 1],                                   # scheduler_policy
                #[10, 60, 100],                            # vm.swappiness
                #[0, 100, 500],                            # vm.vfs_cache_pressure
                #[5, 50],                                  # vm,dirty_background_ratio
                #[10, 80],                                 # vm.dirty_ratio 

                ]
        permutation = list(itertools.product(*bounds))
        return (
                [list(x) for x in permutation],
                [{"o1":False, "o2":False} for _ in permutation],
                [{"o1":False, "o2":False} for _ in permutation])

class ConfigSynthetic:
    """This class is used to create configuration space for synthetic cases
    """
    def __init__(self):
        print ("[STATUS]: initializing configsynthetic class")
        self.n_var = 3

    def set_design_space(self):
        """This function is used to set design space for synthetic functions"""

        self.X = np.random.random((100,self.n_var))
        return (
                [list(i) for i in self.X],
                [{"o1":False, "o2":False} for _ in self.X],
                [{"o1":False, "o2":False} for _ in self.X])

    def set_evaluation(self):
        """This function is used to evaluate synthetic objective functions"""
        from objective_synthetic import ObjectiveSynthetic
        OS=ObjectiveSynthetic()
        (Y1,
        Y2) = OS.Kursawe(self.X, self.n_var)
        Y1=[[i] for i in Y1]
        Y2=[[i] for i in Y2]

        (init_X,
        init_Y1,
        init_Y2,
        init_index)=OS.initialize(self.X,
                     Y1,
                     Y2)
        return (
                Y1,
                Y2,
                init_X,
                init_Y1,
                init_Y2,
                init_index)

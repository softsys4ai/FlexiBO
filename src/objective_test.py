from sklearn.ensemble import RandomForestRegressor
import numpy as np
class ObjectiveTest:
    """This class is used to create objective space for test cases"""
    def __init__(self):
        print "[STATUS]: initializing objectivetest class"

    def fit_rf(
               self,
               X,
               Y1,
               Y2):
        """This function is used to predict"""
        rf1 = RandomForestRegressor(n_estimators = 128)
        rf2 = RandomForestRegressor(n_estimators = 128)
        rf1.fit(X, Y1)
        rf2.fit(X, Y2)
        return (
                rf1,
                rf2)

    def prepare_training_data(
                              self,
                              df,
                              m1,
                              m2):
        """This function is used to prepare training data"""
        X = df[[
                'core0_status',
                'core1_status',
                'core2_status',
                'core3_status',
                'core_freq',
                'gpu_freq',
                'emc_freq']].values

        Y1 = df[m1].values
        Y2 = df[m2].values
        Y1 = [[i] for i in Y1]
        Y2 = [[i] for i in Y2]

        return (
                X,
                Y1,
                Y2)

    def initialize(
                   self,
                   X,
                   Y1,
                   Y2):
        """This function is used to initialize data"""
        import random
        index = random.sample(range(0, len(X) - 1), 1)
        X = [X[i] for i in index]
        Y1 = [Y1[i] for i in index]
        Y2 = [Y2[i] for i in index]
        return (
                X,
                Y1,
                Y2,
                index)

    def measurement(self,
                    rf,
                    x):
        """This function is used for measurement"""
        x = np.array(x)
        y = np.array(rf.predict([x]))
        return x, y

from __future__ import division
import autograd.numpy as anp

class ObjectiveSynthetic:
    """This class is used to create objective space for synthetic cases"""
    def __init__(self):
        print "[STATUS]: initializing objectivesynthetic class"

    def ZDT1(self,
             x,
             n_var):
        """This function is used to define ZDT1 synthetic function"""
        f1 = x[:, 0]
        g = 1 + 9.0 / (n_var - 1) * anp.sum(x[:, 1:], axis=1)
        f2 = g * (1 - anp.power((f1 / g), 0.5))
        return (f1,
                f2)

    def ZDT6(self,
             x,
             n_var):
        """This function is used to define ZDT6 synthetic function"""
        f1 = 1 - anp.exp(-4 * x[:, 0]) * anp.power(anp.sin(6 * anp.pi * x[:, 0]), 6)
        g = 1 + 9.0 * anp.power(anp.sum(x[:, 1:], axis=1) / (n_var - 1.0), 0.25)
        f2 = g * (1 - anp.power(f1 / g, 2))
        return (f1,
                f2)

    def Kursawe(self,
                x,
                n_var):
        """This function is used to define Kursawe synthetic function"""
        l = []
        for i in range(2):
            l.append(-10 * anp.exp(-0.2 * anp.sqrt(anp.square(x[:, i]) + anp.square(x[:, i + 1]))))
        f1 = anp.sum(anp.column_stack(l), axis=1)

        f2 = anp.sum(anp.power(anp.abs(x), 0.8) + 5 * anp.sin(anp.power(x, 3)), axis=1)
        return (f1,
                f2)

    def initialize(
                  self,
                  X,
                  Y1,
                  Y2):
        """This function is used to initialize data"""
        import random
        index = random.sample(range(0, len(X) - 1), 10)
        X = [X[i] for i in index]
        Y1 = [Y1[i] for i in index]
        Y2 = [Y2[i] for i in index]
        return (
                X,
                Y1,
                Y2,
                index)

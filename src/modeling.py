#! /usr/bin/env python2.7
import GPy

class Modeling:
    """This class is used for surrogate models
    """
    def __init__(self):
        print "[STATUS]: initializing modeling class"
        self.INPUT_DIM=7
        self.OUTPUT_DIM=1

    def fit_gp(self,
             X,
             Y):
        """This function is used to fit GP into data
        """
        self.kernel=GPy.kern.Matern52(input_dim=self.INPUT_DIM)
        gp_model=GPy.models.GPRegression(X,Y,self.kernel)
        return gp_model

    def get_gp_model_params(self,
                            gp_model,
                            x):
        [mu,sigma] = gp_model.predict(x,full_cov=1)
        return mu[0,0], sigma[0,0]

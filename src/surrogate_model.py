import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor 
from sklearn.gaussian_process.kernels import ConstantKernel, RBF
from sklearn.ensemble import RandomForestRegressor
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize

class GPSurrogateModel:
    """This class is used for GP surrogate models 
    """
    def __init__(self):
        print ("[STATUS]: Intitializing GPSurrogateModel class")
           
    def fit_gp(self):
        """This function is used to fit GP into data
        """
        
        rbf=ConstantKernel(1.0)*RBF(length_scale=1.0)
        gpr1=GaussianProcessRegressor(kernel=rbf, n_restarts_optimizer=9)
        gpr2=GaussianProcessRegressor(kernel=rbf, n_restarts_optimizer=9)
        
        return gpr1, gpr2
    
    def get_gp_model_params(self, model, x):
        """This function is used to get mean and standard deviation
        """
        [mu,sigma] = model.predict(x,full_cov=1)
        return mu[0,0], sigma[0,0]

class RFSurrogateModel:
    """This class is used for RF surrogate models
    """
    def __init__(self):
        print ("[STATUS]: Initializing RFSurrogateModel class")
    
    def fit_rf(self):
        """This function is used to fit RF into data
        """
        rf1=RandomForestRegressor()
        rf2=RandomForestRegressor()
        return rf1, rf2 
    
    def get_rf_model_params(self, model, x, ntrees):
        """This function is used to get mean and standard deviation
        """
        tree_pred=[tree.predict(x)[0] for tree in model.estimators_]
        mu= np.mean(tree_pred)
        sigma=np.std(tree_pred)
        return mu, sigma 

class TuneSurrogateHyperparams:
    """This class is used to tune hyperparameters of the surrogate models 
    """
    def __init__(self):
        print ("[STATUS]: Initializing TuneSurrogateHyperparams class")
    
    def tune_params(self, space, model, 
                   x, y):
        """This function is used to perform the auto tuning
        """
        
        @use_named_args(space)
        def objective(**params):
            reg.set_params(**params)
            return -np.mean(cross_val_score(model, x, y, 
                                            cv=5, n_jobs=-1, scoring="neg_mean_absolute_error"))

        res = gp_minimize(objective, space, n_calls=50, random_state=0)
        return res 
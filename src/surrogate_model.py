from sklearn.gaussian_process import GaussianProcessRegressor 
from sklearn.gaussian_process.kernels import ConstantKernel, RBF

class GPSurrogateModel:
    """This class is used for surrogate models 
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
    
    def get_gp_model_params(self, 
                            model,
                            x):
        [mu,sigma] = model.predict(x,full_cov=1)
        return mu[0,0], sigma[0,0]
    
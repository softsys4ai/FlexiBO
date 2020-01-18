import GPy

class SurrogateModel:
    """This class is used for surrogate models 
    """
    def __init__(self):
        print ("Intitializing SurrogateModel class")
        self.INPUT_DIM=4
        self.OUTPUT_DIM=1
           
    def fit_gp(self,
             X,
             Y):
        """This function is used to fit GP into data
        """
        self.kernel=GPy.kern.RBF(input_dim=self.INPUT_DIM, variance=1.0,lengthscale=1.0)
        model=GPy.models.GPRegression(X,Y,self.kernel)
        
        return model
    
    def get_gp_model_params(self, 
                            model,
                            x):
        [mu,sigma] = model.predict(x,full_cov=1)
        return mu[0,0], sigma[0,0]
    
import GPy

class GP:
    """This class is used to implement gaussian process regression
    """
    def __init__(self):
        print ("Intitializing GP class")
        self.INPUT_DIM=7
        self.OUTPUT_DIM=1
        self.kernel=GPy.kern.Matern52(input_dim=self.INPUT_DIM)
    
    def fit(self,
             X,
             Y):
        """This function is used to fit GP into data
        """
        model=GPy.models.GPRegression(X,Y,self.kernel)
        return model
    
    def get_model_params(self, 
                         model,
                         x):
        [mu,sigma] = model.predict(x,full_cov=1)
        return mu[0,0], sigma[0,0]

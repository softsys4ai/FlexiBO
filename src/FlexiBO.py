import math
import Config
import numpy as np
from Utils import Utils
from GP import GP
from sklearn.ensemble import RandomForestRegressor

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
                data):
        print ("Initializing FlexiBO class")
        self.utils=Utils()
        self.df=data
        (self.E, self.O, self.measurement)=self.utils.create_design_space(Config.bounds)
        self.NUM_ITER=5
        self.NUM_OBJ=2
        self.m1="inference_time"
        self.m2="temperature"
        self.gp=GP()
        (self.X, self.Y1, self.Y2)=self.prepare_training_data()
        self.fit_rf()
        self.perform_bo_loop()
        
    
    def fit_rf(self):
        """This function is used to predict 
        """
        self.rf1=RandomForestRegressor(n_estimators=16)
        self.rf2=RandomForestRegressor(n_estimators=16)
        self.rf1.fit(self.X,self.Y1)
        self.rf2.fit(self.X,self.Y2)
        
    def prepare_training_data(self):
        """This function is used to prepare training data
        """
        X=self.df[['core0_status',
                         'core1_status', 
                         'core2_status', 
                         'core3_status',
                         'core_freq',
                         'gpu_freq',
                         'emc_freq']].values
        
        Y1=self.df[self.m1].values
        Y2=self.df[self.m2].values
        Y1=[[i] for i in Y1]
        Y2=[[i] for i in Y2]
        
        return (X,
                Y1,
                Y2)
    
    def initialize(self):
        """This function is used to initialize data
        """
        import random
        index=random.sample(range(0,len(self.X)-1),760)
        X=[self.X[i] for i in index]
        Y1=[self.Y1[i] for i in index]
        Y2=[self.Y2[i] for i in index]
        return (X,
                Y1,
                Y2)
    
    def perform_bo_loop(self):
        """This function is used to perform bayesian optimization loop
        PESS_P: Pessimistic Pareto Set
        AVG_P: Average Pareto Set
        OPT_P: Optimistic Pareto Set
        U: Undecided Set
        S: Evaluated Set
        R: Uncertainty Region for each configuration in design space
        """
        # Initialization
        BETA=1.0
        P=list()
        U=list()
        S=list()
        (init_X, init_Y1, init_Y2)=self.initialize()
        (init_X, init_Y1, init_Y2)=(
                                    np.array(init_X), 
                                    np.array(init_Y1), 
                                    np.array(init_Y2)
                                    )
        
        U=np.array(self.E[:])
        # bo loop
        for iteration in xrange(self.NUM_ITER):
            REGION=[{} for _ in U]
            # Fit a GP for each objective
            model_o1=self.gp.fit(init_X,init_Y1)
            model_o2=self.gp.fit(init_X,init_Y2)
            for config in xrange(len(U)):
                # Compute mu and sigma of each points for each objective 
                cur=np.array([U[config]])
                cur_eval=self.O[config]
      
                # Objective 1
                if cur_eval["o1"] is False:
                    (mu_o1,sigma_o1)=self.gp.get_model_params(model_o1,cur)
                else:
                    (mu_o1,sigma_o1)=(self.measurement[config]["o1"],0)
            
                # Objective 2
                if cur_eval["o2"] is False:
                    (mu_o2,sigma_o2)=self.gp.get_model_params(model_o2,cur)
                else:
                    (mu_o2,sigma_o2)=(self.measurement[config]["o2"],0)
                
                # Compute uncertainty region for each point using mu and sigma
                REGION[config]["pes"]=[
                                       0 if (mu_o1-math.sqrt(BETA)*sigma_o1)<0 else mu_o1-math.sqrt(BETA)*sigma_o1,
                                       0 if (mu_o2-math.sqrt(BETA)*sigma_o2)<0 else mu_o2-math.sqrt(BETA)*sigma_o2
                ]
                REGION[config]["avg"]=[mu_o1,mu_o2]
                REGION[config]["opt"]=[
                                       mu_o1+math.sqrt(BETA)*sigma_o1,
                                       mu_o2+math.sqrt(BETA)*sigma_o2
                                      ]
            # Determine undominated points
            (undominated_points_ind,
            undominated_points)=self.utils.identify_undominated_points(REGION)
            # Determine pessimistic, average and optimistic pareto front
            (pes_pareto,
            opt_pareto)=self.utils.construct_pareto_front(undominated_points_ind,
                                                          undominated_points)
            # Determine next configuration and objective
                 
            # Update init_X and init_Y
            break
            
          
        
       

import math
import Config
import numpy as np
from Utils import Utils
from Sample import Sample
from SurrogateModel import SurrogateModel
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
        self.sample=Sample()
        self.df=data
        (self.E, self.O, self.measurement)=self.utils.create_design_space(Config.bounds)
        self.NUM_ITER=5
        self.NUM_OBJ=2
        self.O1_IND=1
        self.O2_IND=0
        self.m1="inference_time"
        self.m2="temperature"
        self.SM=SurrogateModel()
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
        index=random.sample(range(0,len(self.X)-1),10)
        X=[self.X[i] for i in index]
        Y1=[self.Y1[i] for i in index]
        Y2=[self.Y2[i] for i in index]
        return (X,
                Y1,
                Y2,
                index)
                           
    def perform_bo_loop(self):
        """This function is used to perform bayesian optimization loop
        U: Design Space
        REGION: Uncertainty Region for each configuration in design space
        """
        # Initialization
        BETA=1.0
        (init_X, init_Y1, init_Y2, init_measured_indices)=self.initialize()
        
        for i in xrange(len(init_measured_indices)):
            self.O[i]["o1"]=True
            self.measurement[init_measured_indices[i]]["o1"]=init_Y1[i][0]
            self.O[i]["o2"]=True
            self.measurement[init_measured_indices[i]]["o2"]=init_Y2[i][0]    
        (init_X, init_Y1, init_Y2)=(
                                    np.array(init_X), 
                                    np.array(init_Y1), 
                                    np.array(init_Y2)
                                    )
        
        U=np.array(self.E[:])
        init_X1=init_X[:]
        init_X2=init_X[:]
     
        # bo loop
        for iteration in xrange(self.NUM_ITER):
            print "---------------------------------------Iteration: ",iteration
            REGION=[{} for _ in U]
            # Fit a GP for each objective
            model_o1=self.SM.fit_gp(init_X1,init_Y1)
            model_o2=self.SM.fit_gp(init_X2,init_Y2)
            for config in xrange(len(U)):
                # Compute mu and sigma of each points for each objective 
                cur=np.array([U[config]])
                cur_eval=self.O[config]
      
                # Objective 1
                if cur_eval["o1"] is False:
                    (mu_o1,sigma_o1)=self.SM.get_gp_model_params(model_o1,cur)
                else:
                    (mu_o1,sigma_o1)=(self.measurement[config]["o1"],0)
            
                # Objective 2
                if cur_eval["o2"] is False:
                    (mu_o2,sigma_o2)=self.SM.get_gp_model_params(model_o2,cur)
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
            
            self.REGION=[
                   {'opt': [2, 11], 'avg': [1, 10], 'pes': [0.5,9]},
                   {'opt': [3, 9], 'avg': [2.5, 8], 'pes': [1.5,7]},
                   {'opt': [1.5, 7], 'avg': [1, 6], 'pes': [0.5,5]},
                   {'opt': [5, 6], 'avg': [4.5, 5], 'pes': [4,4]},
                   {'opt': [7.5, 4], 'avg': [6.5, 3], 'pes': [6,2.5]},
                   {'opt': [3.5, 3.5], 'avg': [3, 3], 'pes': [2.5,2.5]},
                   {'opt': [5.5, 3], 'avg': [5, 2], 'pes': [4.5,1.5]}
                   ] 
            
            # Determine undominated points
            (undominated_points_ind,
            undominated_points)=self.utils.identify_undominated_points(self.REGION)
            # Determine pessimistic pareto front
            (pess_pareto,
            pess_indices_map)=self.utils.construct_pessimistic_pareto_front(undominated_points_ind,undominated_points,"CONSTRUCT")
            # Determine optimistic pareto front
            (opt_pareto,
            opt_indices_map)=self.utils.construct_optimistic_pareto_front(undominated_points_ind,undominated_points,"CONSTRUCT")
            # Determine pessimistic pareto volume
            pess_pareto_volume=self.utils.compute_pareto_volume(pess_pareto)
            # Determine optimistic pareto volume
            opt_pareto_volume=self.utils.compute_pareto_volume(opt_pareto)
            # Determine volume of the pareto front
            volume_of_pareto_front=opt_pareto_volume-pess_pareto_volume
            # Determine next configuration and objective
            (next_sample_index, next_sample, objective)=self.sample.determine_next_sample(pess_pareto,
                                                                                          opt_pareto,
                                                                                          pess_indices_map,
                                                                                          opt_indices_map,
                                                                                          pess_pareto_volume,
                                                                                          opt_pareto_volume,
                                                                                          REGION,
                                                                                          self.E)
            
            # Perform measurement on next sample on the objective returned
            # Update init_X and init_Y
            if objective=="o1":
                cur_X1=np.array(next_sample)
                cur_Y1=np.array(self.rf1.predict([cur_X1]))
                self.O[next_sample_index]["o1"]=True
                self.measurement[next_sample_index]["o1"]=cur_Y1[0]
                np.vstack((init_X1,cur_X1))
                np.vstack((init_Y1,cur_Y1))
            if objective=="o2":
                cur_X2=np.array(next_sample)
                cur_Y2=np.array(self.rf2.predict([cur_X2]))
                self.O[next_sample_index]["o2"]=True
                self.measurement[next_sample_index]["o2"]=cur_Y2[0]
                np.vstack((init_X2,np.array(next_sample)))
                np.vstack((init_Y2,cur_Y2))
            
                   

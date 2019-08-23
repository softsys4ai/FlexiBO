from __future__ import division
import math
import Config
import numpy as np
from Utils import Utils
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
        self.df=data
        (self.E, self.O, self.measurement)=self.utils.create_design_space(Config.bounds)
        self.NUM_ITER=5
        self.NUM_OBJ=2
        self.O1_IND=1
        self.O2_IND=0
        self.m1="inference_time"
        self.m2="temperature"
        self.O1_COST=1
        self.O2_COST=self.O1_COST*8
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
        index=random.sample(range(0,len(self.X)-1),760)
        X=[self.X[i] for i in index]
        Y1=[self.Y1[i] for i in index]
        Y2=[self.Y2[i] for i in index]
        return (X,
                Y1,
                Y2)
    
    def determine_next_sample(self,
                             pess_pareto,
                             opt_pareto,
                             pess_indices_map,
                             opt_indices_map,
                             pess_pareto_volume,
                             opt_pareto_volume):
        """This function is used to determine next sample
        """
        if pess_indices_map==opt_indices_map:
            indices_map=pess_indices_map
        pess_ind=[indices_map[i] for i in xrange(len(pess_pareto))]
        opt_ind=[indices_map[i] for i in xrange(len(opt_pareto))]
        
        pess_status=[[{"pess":True,"opt":True}] if i in opt_ind else [{"pess":True,"opt":False}] for i in pess_ind]
        opt_status=[[{"pess":True,"opt":True}] if i in pess_ind else [{"pess":False,"opt":True}] for i in opt_ind]
        
        # compute dv/c for each point in pessimistic pareto front
        dv_per_cost_pess=[{"o1":0,"o2":0} for i in pess_ind]
        for i in xrange(len(pess_pareto)):                   
             for j in xrange(self.NUM_OBJ):
                         
                 if pess_status[i][0]["pess"] is True:
                     # Update pessimistic pareto front 
                     cur_pess=pess_pareto[:]
                     # replace pess with avg value across O1
                     cur_pess[i][j]=self.REGION[pess_ind[i]]["avg"][j]
                     cur_pess_pareto=self.utils.construct_pessimistic_pareto_front(pess_ind,
                                                                              cur_pess,
                                                                              "UPDATE")
                     cur_pess_volume=self.utils.compute_pareto_volume(cur_pess_pareto)
                 
                 if pess_status[i][0]["opt"] is True:
                     # Update optimistic pareto front 
                     cur_opt=opt_pareto[:]
                     opt_i=opt_ind.index(pess_ind[i])
                     # replace opt with avg value across O1
                     cur_opt[opt_i][j]=self.REGION[opt_ind[i]]["avg"][j]
                     cur_opt_pareto=self.utils.construct_optimistic_pareto_front(opt_ind,
                                                                                 cur_opt,
                                                                                 "UPDATE")
                     cur_opt_volume=self.utils.compute_pareto_volume(cur_opt_pareto)
                 
                 if pess_status[i][0]["opt"] is False:
                     # No update
                     cur_opt_volume=opt_pareto_volume
                 
                 dv=(opt_pareto_volume-pess_pareto_volume)-(cur_opt_volume-cur_pess_volume)
                 if j==self.O1_IND:
                     dv_per_cost_pess[i]["o1"]=dv/self.O1_COST
                 if j==self.O2_IND:
                     dv_per_cost_pess[i]["o2"]=dv/self.O2_COST
        
        # compute dv/c for each point in pessimistic pareto front
        dv_per_cost_opt=[{"o1":0,"o2":-0} for i in opt_ind]
        for i in xrange(len(opt_pareto)):                   
             for j in xrange(self.NUM_OBJ):
                         
                 if (opt_status[i][0]["opt"] is True and 
                     opt_status[i][0]["opt"] is False):
                     
                     cur_opt=opt_pareto[:]
                     # replace pess with avg value across O1
                     cur_opt[i][j]=self.REGION[opt_ind[i]]["avg"][j]
                     cur_opt_pareto=self.utils.construct_optimistic_pareto_front(opt_ind,
                                                                              cur_opt,
                                                                              "UPDATE")
                     cur_opt_volume=self.utils.compute_pareto_volume(cur_opt_pareto)
                     cur_pess_volume=pess_pareto_volume
                 
                 dv=(opt_pareto_volume-pess_pareto_volume)-(cur_opt_volume-cur_pess_volume)
                 if j==self.O1_IND:
                     dv_per_cost_pess[i]["o1"]=dv/self.O1_COST
                 if j==self.O2_IND:
                     dv_per_cost_pess[i]["o2"]=dv/self.O2_COST         
              
                 
                            
    def perform_bo_loop(self):
        """This function is used to perform bayesian optimization loop
        U: Undecided Set
        S: Evaluated Set
        REGION: Uncertainty Region for each configuration in design space
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
            model_o1=self.SM.fit_gp(init_X,init_Y1)
            model_o2=self.SM.fit_gp(init_X,init_Y2)
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
            """
            self.REGION=[
                   {'opt': [2, 11], 'avg': [1, 10], 'pes': [0.5,9]},
                   {'opt': [3, 9], 'avg': [2.5, 8], 'pes': [1.5,7]},
                   {'opt': [1.5, 7], 'avg': [1, 6], 'pes': [0.5,5]},
                   {'opt': [5, 6], 'avg': [4.5, 5], 'pes': [4,4]},
                   {'opt': [7.5, 4], 'avg': [6.5, 3], 'pes': [6,2.5]},
                   {'opt': [3.5, 3.5], 'avg': [3, 3], 'pes': [2.5,2.5]},
                   {'opt': [5.5, 3], 'avg': [5, 2], 'pes': [4.5,1.5]}
                   ] 
            """
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
            next_sample=self.determine_next_sample(pess_pareto,
                                                   opt_pareto,
                                                   pess_indices_map,
                                                   opt_indices_map,
                                                   pess_pareto_volume,
                                                   opt_pareto_volume)
            
            # Update init_X and init_Y
            break
            
          
        
       

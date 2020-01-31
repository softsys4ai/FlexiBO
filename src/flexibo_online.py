"""-----------------------------------------------------------------------------
@Name: Flexible Bayesian Optimization (FlexiBO): An active learning for optimiz-
ing  multiple objectives of different cost
@Version: 0.1
@Author: Shahriar Iqbal
--------------------------------------------------------------------------------
"""
import os 
import math
import numpy as np
from src.Utils import Utils
from src.Sample import Sample
from src.Config import ConfigReal
from src.config_hardware import ConfigHardware
from src.config_network import ConfigNetwork
from src.compute_performance import ComputePerformance 
from src.SurrogateModel import SurrogateModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor 
from sklearn.gaussian_process.kernels import ConstantKernel, RBF
 
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
        cfg=ConfigReal()
        (
        self.E, 
        self.O, 
        self.measurement)=cfg.set_design_space()
        
        self.NUM_ITER=200
        self.NUM_OBJ=2
        self.O1_IND=0
        self.O2_IND=1
        self.m1="inference_time"
        self.m2="power_consumption"
        self.SM=SurrogateModel()
        (
        self.X, 
        self.Y1, 
        self.Y2)=self.prepare_training_data()
        self.fit_rf()
        self.perform_bo_loop()
        
    def fit_rf(self):
        """This function is used to predict 
        """
        self.rf1=RandomForestRegressor(n_estimators=16)
        self.rf2=RandomForestRegressor(n_estimators=16)
        self.rf1.fit(self.X, self.Y1)
        self.rf2.fit(self.X, self.Y2)
        
    def prepare_training_data(self):
        """This function is used to prepare training data
        """
    
        X=self.df[['number_of_cores',
                   'core_freq',
                   'gpu_freq',
                   'emc_freq']].values
        
        Y1=self.df[self.m1].values
        Y2=self.df[self.m2].values
        Y1=[[i] for i in Y1]
        Y2=[[i] for i in Y2]
        
        return (X, Y1, Y2)
    
    def initialize(self):
        """This function is used to initialize data
        """
        import random
        index=random.sample(range(0,len(self.X)-1),10)
        X=[self.X[i] for i in index]
        Y1=[self.Y1[i] for i in index]
        Y2=[self.Y2[i] for i in index]
        return (X, Y1, Y2,
                index)
                           
    def perform_bo_loop(self):
        """This function is used to perform bayesian optimization loop
        U: Design Space
        REGION: Uncertainty Region for each configuration in design space
        """
        # Initialization
        BETA=1.0
        (init_X, init_Y1, init_Y2, init_measured_indices)=self.initialize()
    
        for i in range(0,len(init_measured_indices)):
            self.O[i]["o1"]=True
            self.measurement[init_measured_indices[i]]["o1"]=init_Y1[i][0]
            self.O[i]["o2"]=True
            self.measurement[init_measured_indices[i]]["o2"]=init_Y2[i][0]    
        (init_X, init_Y1, init_Y2)=(np.array(init_X), np.array(init_Y1), np.array(init_Y2))
        
        U=np.array(self.E[:])
        init_X1=init_X[:]
        init_X2=init_X[:]
        rbf=ConstantKernel(1.0)*RBF(length_scale=1.0)
        gpr1=GaussianProcessRegressor(kernel=rbf, n_restarts_optimizer=9)
        gpr2=GaussianProcessRegressor(kernel=rbf, n_restarts_optimizer=9)
        print (init_X)
        # bo loop
        for iteration in range(0,self.NUM_ITER):
            print ("---------------------------------------Iteration: ",iteration)
            REGION=[{} for _ in U]
            
            # Fit a GP for each objective
            model_o1=self.SM.fit_gp(init_X1,init_Y1)
            model_o2=self.SM.fit_gp(init_X2,init_Y2)
            #model_o1=gpr1.fit(init_X1,init_Y1)
            #model_o2=gpr2.fit(init_X2,init_Y2)
            
            for config in range(0,len(U)):
                # Compute mu and sigma of each points for each objective 
                cur=np.array([U[config]])
                cur_eval=self.O[config]
                # Objective 1
                if cur_eval["o1"] is False:
                    (mu_o1,sigma_o1)=self.SM.get_gp_model_params(model_o1,cur)
                    #mu_o1, sigma_o1= model_o1.predict(cur,return_std=True)
                    
                else:
                    (mu_o1,sigma_o1)=(self.measurement[config]["o1"],0)
                 
                # Objective 2
                if cur_eval["o2"] is False:
                    (mu_o2,sigma_o2)=self.SM.get_gp_model_params(model_o2,cur)                   
                    #mu_o2, sigma_o2= model_o2.predict(cur,return_std=True)[0]
                else:
                    (mu_o2,sigma_o2)=(self.measurement[config]["o2"],0)
                
                # Compute uncertainty region for each point using mu and sigma                
                REGION[config]["pes"]=[
                0 if (mu_o1-math.sqrt(BETA)*sigma_o1)<0 else mu_o1-math.sqrt(BETA)*sigma_o1,
                0 if (mu_o2-math.sqrt(BETA)*sigma_o2)<0 else mu_o2-math.sqrt(BETA)*sigma_o2
                ]
                REGION[config]["avg"]=[mu_o1,mu_o2]
                REGION[config]["opt"]=[mu_o1+math.sqrt(BETA)*sigma_o1, mu_o2+math.sqrt(BETA)*sigma_o2]
            
           
            # Determine undominated points
            (undominated_points_ind,
            undominated_points)=self.utils.identify_undominated_points(REGION)
            # Determine pessimistic pareto front
            (pess_pareto,
            pess_indices_map)=self.utils.construct_pessimistic_pareto_front(
                                undominated_points_ind, undominated_points, "CONSTRUCT")
            # Determine optimistic pareto front
            (opt_pareto,
            opt_indices_map)=self.utils.construct_optimistic_pareto_front(
                                undominated_points_ind, undominated_points, "CONSTRUCT")
            # Determine pessimistic pareto volume
            pess_pareto_volume=self.utils.compute_pareto_volume(pess_pareto)
            # Determine optimistic pareto volume
            opt_pareto_volume=self.utils.compute_pareto_volume(opt_pareto)
            # Determine volume of the pareto front
            volume_of_pareto_front=opt_pareto_volume-pess_pareto_volume
            # Determine next configuration and objective
            (next_sample_index, 
            next_sample, 
            objective)=self.sample.determine_next_sample(pess_pareto, opt_pareto, pess_indices_map,
                                                         opt_indices_map, pess_pareto_volume, opt_pareto_volume,
                                                         REGION, self.E)
            
            # Perform measurement on next sample on the objective returned
            # Update init_X and init_Y
            
            
            if objective=="o1":
                # Evaluate Objective O1
                ConfigHardware(next_sample)
                ComputePerformance()
                cur_X1=np.array(next_sample)               
                
                #cur_Y1=np.array(self.rf1.predict([cur_X1]))
                self.O[next_sample_index]["o1"]=True
                self.measurement[next_sample_index]["o1"]=cur_Y1[0]
                np.vstack((init_X1,cur_X1))
                np.vstack((init_Y1,cur_Y1))
            if objective=="o2":
                cur_X2=np.array(next_sample)
                ConfigNetwork()
                ComputePerformance()
                cur_Y2=np.array(self.rf2.predict([cur_X2]))
                self.O[next_sample_index]["o2"]=True
                self.measurement[next_sample_index]["o2"]=cur_Y2[0]
                np.vstack((init_X2,np.array(next_sample)))
                np.vstack((init_Y2,cur_Y2))
            
                   
import os 
import sys
import subprocess
import time
import json
import yaml
import numpy as np
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler

class ComputePerformance(object):
    """This function is used to compute accuracy and energy consumption
    """
    def __init__(self):
        print ("[STATUS]: Initializing Compute Performance Class")
        with open("config.yaml") as fp:
            self.cfg=yaml.load(fp)
        self.cur_sys="TX2"
        self.model=self.get_model()
        (self.x_test, self.y_test)=self.get_test_data()
        self.total_power=list()
       
        # create scheduler
        job_defaults= {"coalesce":False,
                       "max_instances":1
        }
        self.sched=BackgroundScheduler(job_defaults=job_defaults)
        # add background job
        self.sched.start()
        self.sched.add_job(self.compute_power,"interval",seconds=.03)       
        # start        
        self.inference_time=self.compute_inference_time()
        # end
        self.sched.shutdown()
    
    
    def compute_power(self):
        """This function is used to read power consumption using from INA monitor 
        """
        filename=self.cfg["config"]["systems"][self.cur_sys]["power"]["total"]
        try:
            
            self.total_power.append(subprocess.getstatusoutput("cat {0}".format(filename))[1])
        except AttributeError:
            print("[ERROR]: invalid power file ")
    
    def compute_inference_time(self):
        """This function is used to compute inference time
        """
        try:
            start=time.time()      
            output=self.model.evaluate(self.x_test,self.y_test)
            
            duration=time.time()-start
            return duration         
        except Exception as e:
            print("[ERROR]: prediction failed due to {0}".format (str(e)))
    
    def get_output_metrics(self):
        """This file is used to return output data 
        """
        
        self.total_power=[int(i) if i is not None else 0 for i in self.total_power ]    
        self.total_power=np.sum(self.total_power)   
        return self.inference_time, self.total_power
        
      

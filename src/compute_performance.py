#!/usr/bin/python
import os 
import sys
import commands
import time
import json
import logging
import numpy as np
from Configuration import Config as cfg
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler

class ComputePerformance(object):
    """This function is used to compute cpu,gpu and total power and measure inference time
    """
    def __init__(self,
                cur_config,
                cur_sys,
                model,
                test_data):
        print ("[STATUS]: Initializing Compute Performance Class")
        
        self.cur_config=cur_config
        
        logging.basicConfig()
        logging.getLogger("apscheduler").setLevel(logging.ERROR)
        self.cur_sys=cur_sys
        self.model=model
        self.test_data=test_data
        self.total_power=list()
      
        # create scheduler
        job_defaults= {"coalesce":False,
                       "max_instances":1
        }
        self.sched=BackgroundScheduler(job_defaults=job_defaults)
        # add background job
        self.sched.start()
        self.sched.add_job(self.compute_power,"interval",seconds=.01)       
        # start        
        self.inference_time=self.compute_inference_time()
        # end
        self.sched.shutdown()
              
    def compute_power(self):
        """This function is used to read power consumption using from INA monitor 
        """
        filename=cfg.systems[self.cur_sys]["power"]["total"]
        try:
            
            self.total_power.append(commands.getstatusoutput("cat {0}".format(filename))[1])
        except AttributeError:
            self.logger.error("[ERROR]: invalid power file ")
    
    def compute_inference_time(self):
        """This function is used to compute inference time
        """
        try:
            start=time.time()      
            output=self.model.predict(self.test_data)
            
            duration=time.time()-start
            return duration         
        except Exception as e:
            self.logger.error("[ERROR]: prediction failed due to {0}".format (str(e)))
    
    def get_output_metrics(self):
        """This file is used to return output data 
        """
        
        self.total_power=[int(i) if i is not None else 0 for i in self.total_power ]    
        self.total_power=np.sum(self.total_power)   
        return self.inference_time, self.total_power
        
          

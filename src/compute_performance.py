import os 
import sys
import subprocess
import time
import json
import numpy as np
from Configuration import Config as cfg
from multiprocessing import Process
from apscheduler.schedulers.background import BackgroundScheduler

class ComputePerformance(object):
    """This function is used to compute cpu,gpu and total power and measure inference time
    """
    def __init__(self):
        print ("[STATUS]: Initializing Compute Performance Class")
        
        self.cur_sys="TX2"
        self.model=self.get_model()
        (self.x_test, self.y_test)=self.get_test_data()
        self.total_power=list()
        print (self.x_test)
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
    
    def get_model(self):
        """This function is used to get model
        """
        from keras.applications import ResNet50
        self.model=ResNet50()

    def get_test_data(self):
        """This function is used to get test data
        """ 
        from keras.datasets import cifar10      
        (_, _), (x_test, y_test) = cifar10.load_data()
        return (x_test,y_test)

    def compute_power(self):
        """This function is used to read power consumption using from INA monitor 
        """
        filename=cfg.systems[self.cur_sys]["power"]["total"]
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
        
ComputePerformance()        

#!/usr/bin/python
import os 
import sys
import commands
import subprocess
from Configuration import Config as cfg

class ConfigNetworkOptions(object):
    """This class is used to create different configuration space for jetson  tx2
    """
    def __init__(self,
                 cur_config):
               
        self.logger.info("[STATUS]: Initializing ConfigNetworkOptions Class")
        self.cur_config=cur_config
                                         
    def set_big_core_status(self,
                            cpu_name,
                            status):
        """This function is used set core status (enable or disable)
        ------------------------------------------------------------------------
        @args:
             cpu_name: cpu that will be enabled or disabled
        @returns:
        boolean: whether the operation was successful or not
        ------------------------------------------------------------------------  
        """
        
        if cpu_name!="cpu0":
            filename="{0}{1}{2}".format("/sys/devices/system/cpu/",
                                       cpu_name,
                                       "/online"
                                       )
            cur_status=commands.getstatusoutput("cat {0}".format(filename))[1]   
            if cur_status!=status:
                res=subprocess.call(["sudo","sh","./measurement/change_core_status.sh",str(cpu_name),str(status)])
                if res!=0:
                    err="subprocess command failed"
                    print("[CPU STATUS ERROR]: {0}".format(err))
                    return False
                # check if the operation is successful
                new_status= commands.getstatusoutput("cat {0}".format(filename))[1]
                if new_status!=status:
                    print ("[CPU STATUS ERROR]: "+cpu_name+ "\n"
                                       "expected: " + str(status) + "\n"
                                       "actual: "+ str(new_status))
                    return False
                return True
        else:
            print("invalid cpu_name argument")



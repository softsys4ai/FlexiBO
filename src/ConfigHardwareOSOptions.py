#!/usr/bin/python
import os 
import sys
import commands
import subprocess
from Configuration import Config as cfg

class ConfigHardwareOSOptions(object):
    """This class is used to create different configuration space for jetson  tx2
    """
    def __init__(self,
                 cur_config,
                 cur_sys,
                 big_cores):
               
        self.logger.info("[STATUS]: Initializing ConfigHardwareOSOptions Class")
        self.cur_config=cur_config
        self.cur_sys=cur_sys
        self.big_cores=big_cores
        # define constant variables
        self.ENABLE="1"
        self.DISABLE="0"
        # set specific configuration
        
        self.set_big_core_status(cfg.systems[self.cur_sys]["cpu"]["cores"]["core1"],self.cur_config[1])
        self.set_big_core_status(cfg.systems[self.cur_sys]["cpu"]["cores"]["core2"],self.cur_config[2])
        self.set_big_core_status(cfg.systems[self.cur_sys]["cpu"]["cores"]["core3"],self.cur_config[3])
        self.set_big_core_freq(cfg.systems[self.cur_sys]["cpu"]["cores"]["core0"],self.cur_config[4])
        
        self.set_gpu_freq(self.cur_config[5])
        self.set_emc_freq(self.cur_config[6])
        self.set_scheduler_policy(self.cur_config[7])
        self.set_vm_swappiness(self.cur_config[8])
        self.set_vm_vfs_cache_pressure(self.cur_config[9])
                                   
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

    def set_big_core_freq(self,
                          cpu_name,
                          frequency):
        """This function is used to set core frequency of one or more cores
        ------------------------------------------------------------------------
        @args:
            frequency: clockspeed at what the cpu will be set 
            cpu_name: cpu number which will be set
        @returns:
            @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        
        if frequency is not None:
            filename="{0}{1}{2}".format("/sys/devices/system/cpu/",
                                        cpu_name,
                                        "/cpufreq/scaling_cur_freq")
            
            cur_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
            res=subprocess.call(["sudo","sh","./measurement/change_core_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
            if res!=0:
                    err="subprocess command failed"
                    print("[CPU FREQUENCY ERROR]: {0}".format(err))
                    return False
            
            new_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
            if str(new_freq)!=str(frequency):
                print ("[CPU FREQUENCY ERROR]: "+cpu_name+ "\n"
                                   "expected: " + str(frequency) + "\n"
                                   "actual: "+ str(new_freq))
                return False 

            return True  
          
    def set_gpu_freq(self,
                     frequency):
        """This function is used to change gpu clockspeeds
        ------------------------------------------------------------------------
        @args:
           frequency: the clockspeed at which the gpu will be set
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        
        if frequency is not None:
            filename=cfg.systems[self.cur_sys]["gpu"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    res=subprocess.call(["sudo","sh","./measurement/change_gpu_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
                    if res!=0:
                        err="subprocess command failed"
                        print("[GPU FREQUENCY ERROR]: {0}".format(err))
                        return False
                           
                    # check if the operation is successful 
                    new_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        print ("[GPU FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                print("[GPU FREQUENCY ERROR: {0}]".format(e)) 
    
    def set_emc_freq(self,
                     frequency):
        """This function is used to change emmc clockspeeds
        ------------------------------------------------------------------------
        @args:
            frequency: the clockspeed at which the emmc will be set
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        
        if frequency is not None:
            filename=cfg.systems[self.cur_sys]["emc"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    
                    res=subprocess.call(["sudo","sh","./measurement/change_emc_frequency.sh",str(self.cur_sys),str(frequency)])
                    if res!=0:
                        err="subprocess command failed"
                        print("[EMC FREQUENCY ERROR]: {0}".format(err))
                        return False
            
                    # check if the operation is successful 
                    new_freq=commands.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        print ("[EMC FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                print("[EMC FREQUENCY ERROR: {0}]".format(e))
   
    def set_scheduler_policy(self,
                             policy):
        """This function is used to set scheduler policy
        ------------------------------------------------------------------------
        @args:
            policy: the policy at which the scheduler will be set
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """                     
        if policy=="cfq":
            os.system ("echo cfq > /sys/block/mmcblk0/queue/scheduler")
            return True                     
        elif policy=="noop":
            os.system ("echo cfq > /sys/block/mmcblk0/queue/scheduler")
            return True
        else:
            print("[SCHEDULER POLICY ERROR]: Unknown Policy ")
            return False                 
        
    def set_vm_swappiness(self,
                          swp_value):
        """This function is used to set vm.swappiness value
        ------------------------------------------------------------------------
        @args:
            swp_value: value of the vm.swappiness
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        cmd="systcl vm.swappiness={0}".format(swp_value)
        os.system (cmd)
        return True
                            
    def set_vm_vfs_cache_pressure(self,
                               cache_pressure):
        """This function is used to set vm.vfs_cache_pressure value
        ------------------------------------------------------------------------
        @args:
            swp_value: value of the vm.vfs_cache_pressure
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        cmd="systcl vm.vfs_cache_pressure={0}".format(cache_pressure)
        os.system (cmd)
        return True 
               

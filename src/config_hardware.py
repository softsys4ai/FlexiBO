import os 
import sys
import yaml
import subprocess

class ConfigHardware(object):
    """This class is used to create different configuration space for jetson  tx2
    """
    def __init__(self,
                 config):
               
        print("[STATUS]: Initializing ConfigHardware Class")
        self.cur_config=self.process(config)
        with open("config.yaml") as fp:
            self.cfg=yaml.load(fp)
        self.cur_sys="TX2"
        # define constant variables
        self.ENABLE="1"
        self.DISABLE="0"
        
        # set specific configuration    
        self.set_big_core_status(self.cfg["config"]["systems"][self.cur_sys]["cpu"]["cores"]["core1"],self.cur_config[1])
        self.set_big_core_status(self.cfg["config"]["systems"][self.cur_sys]["cpu"]["cores"]["core2"],self.cur_config[2])
        self.set_big_core_status(self.cfg["config"]["systems"][self.cur_sys]["cpu"]["cores"]["core3"],self.cur_config[3])
        
        self.set_big_core_freq(self.cfg["config"]["systems"][self.cur_sys]["cpu"]["cores"]["core0"],self.cur_config[4])  
        self.set_gpu_freq(self.cur_config[5])
        self.set_emc_freq(self.cur_config[6])
        
        #self.set_scheduler_policy(self.cur_config[7])
        self.set_vm_swappiness(self.cur_config[7])
        self.set_vm_vfs_cache_pressure(self.cur_config[8])
        self.set_vm_dirty_background_ratio(self.cur_config[9])
        self.set_vm_dirty_ratio(self.cur_config[10])

    def process(self, cur_config):
        """This function is used to process the current configuration
        @args:
            cur_config: current hardware configuration
        @returns:
            proc_cur_config: processed current configuration
        """
        if cur_config[0]==1:
            proc_config=[1,0,0,0]
        elif cur_config[0]==2:
            proc_config=[1,1,0,0]
        elif cur_config[0]==3:
            proc_config=[1,1,1,0]
        elif cur_config[0]==4:
            proc_config=[1,1,1,1]
        
        else:
            print("[ERROR]: Invalid Configuration")
        proc_config.extend(cur_config[1:8])
        return proc_config
            

    def set_big_core_status(self, cpu_name, status):
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
            cur_status=subprocess.getstatusoutput("cat {0}".format(filename))[1]   
            if cur_status!=status:
                res=subprocess.call(["sudo","sh","./measurement/change_core_status.sh",str(cpu_name),str(status)])
                if res!=0:
                    err="subprocess command failed"
                    print("[CPU STATUS ERROR]: {0}".format(err))
                    return False
                # check if the operation is successful
                new_status= subprocess.getstatusoutput("cat {0}".format(filename))[1]
                if new_status!=status:
                    print ("[CPU STATUS ERROR]: "+cpu_name+ "\n"
                                       "expected: " + str(status) + "\n"
                                       "actual: "+ str(new_status))
                    return False
                return True
        else:
            print("invalid cpu_name argument")

    def set_big_core_freq(self, cpu_name, frequency):
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
            
            cur_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
            res=subprocess.call(["sudo","sh","./measurement/change_core_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
            if res!=0:
                    err="subprocess command failed"
                    print("[CPU FREQUENCY ERROR]: {0}".format(err))
                    return False
            
            new_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
            if str(new_freq)!=str(frequency):
                print ("[CPU FREQUENCY ERROR]: "+cpu_name+ "\n"
                                   "expected: " + str(frequency) + "\n"
                                   "actual: "+ str(new_freq))
                return False 

            return True  
          
    def set_gpu_freq(self, frequency):
        """This function is used to change gpu clockspeeds
        ------------------------------------------------------------------------
        @args:
           frequency: the clockspeed at which the gpu will be set
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        
        if frequency is not None:
            filename=self.cfg["config"]["systems"][self.cur_sys]["gpu"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    res=subprocess.call(["sudo","sh","./measurement/change_gpu_frequency.sh",str(self.cur_sys),str(frequency),str(cur_freq)])
                    if res!=0:
                        err="subprocess command failed"
                        print("[GPU FREQUENCY ERROR]: {0}".format(err))
                        return False
                           
                    # check if the operation is successful 
                    new_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        print ("[GPU FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                print("[GPU FREQUENCY ERROR: {0}]".format(e)) 
    
    def set_emc_freq(self, frequency):
        """This function is used to change emmc clockspeeds
        ------------------------------------------------------------------------
        @args:
            frequency: the clockspeed at which the emmc will be set
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        
        if frequency is not None:
            filename=self.cfg["config"]["systems"][self.cur_sys]["emc"]["frequency"]["current"]
            try:
                if frequency is not None:
                    cur_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    
                    res=subprocess.call(["sudo","sh","./measurement/change_emc_frequency.sh",str(self.cur_sys),str(frequency)])
                    if res!=0:
                        err="subprocess command failed"
                        print("[EMC FREQUENCY ERROR]: {0}".format(err))
                        return False
            
                    # check if the operation is successful 
                    new_freq=subprocess.getstatusoutput("cat {0}".format(filename))[1]
                    if new_freq!=frequency:
                        print ("[EMC FREQUENCY ERROR]: \n"
                                           "expected: " + str(frequency) + "\n"
                                           "actual: "+ str(new_freq))
                        return False

                    return True
            except AttributeError as e:
                print("[EMC FREQUENCY ERROR: {0}]".format(e))
   
    def set_scheduler_policy(self,policy):
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
        
    def set_vm_swappiness(self, swp_value):
        """This function is used to set vm.swappiness value
        ------------------------------------------------------------------------
        @args:
            swp_value: value of the vm.swappiness
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        cmd="sysctl vm.swappiness={0}".format(swp_value)
        os.system (cmd)
        return True
                            
    def set_vm_vfs_cache_pressure(self, cache_pressure):
        """This function is used to set vm.vfs_cache_pressure value
        ------------------------------------------------------------------------
        @args:
            swp_value: value of the vm.vfs_cache_pressure
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        cmd="sysctl vm.vfs_cache_pressure={0}".format(cache_pressure)
        os.system (cmd)
        return True 
    
    def set_vm_dirty_background_ratio(self, dirty_bg_val):
        """This function is used to set vm.vfs_dirty_background_ratio
        ------------------------------------------------------------------------
        @args:
            dirty_bg_val: value of the vm.vfs_dirty_background_ratio
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        cmd="sysctl vm.dirty_background_ratio={0}".format(dirty_bg_val)
        os.system (cmd)
        return True 
    
    def set_vm_dirty_ratio(self, dirty_val):
        """This function is used to set vm.dirty_ratio
        ------------------------------------------------------------------------
        @args:
            dirty_val: value of the vm.vfs_dirty_ratio
        @returns:
            boolean: status of operation
        ------------------------------------------------------------------------
        """
        cmd="sysctl vm.dirty_ratio={0}".format(dirty_val)
        os.system (cmd)
        return True 
               

#!/usr/bin/python
import os 
import sys
import paramiko
import traceback 
import yaml

class ConfigNetwork(object):
    """This class is used to 
    """
    def __init__(self, cur_net, cur_config):
               
        self.cur_config=cur_config
        self.network=cur_net
        with open("config.yaml") as fp:
            cfg=yaml.load(fp)
        # host
        self.host=cfg["config"]["online"]["remote"]["host"]
        # username
        self.user=cfg["config"]["online"]["remote"]["user"]
        # password
        self.passwd=cfg["config"]["online"]["remote"]["pass"]
        # keyfile
        self.keyfile=cfg["config"]["online"]["remote"]["keyfile"]
        # remote code directory
        self.remote_code_dir=cfg["config"]["online"]["remote"]["network"]["code_dir"]
        self.remote_code_dir=self.remote_code_dir.replace("network",cur_net)
        # remote model directory
        self.remote_model_dir=cfg["config"]["online"]["remote"]["network"]["model_dir"]
        self.remote_model_dir=self.remote_model_dir.replace("network",cur_net)
        # remote current configuration directory
        self.remote_conf_dir=cfg["config"]["online"]["remote"]["network"]["conf_dir"]
        self.remote_conf_dir=self.remote_conf_dir.replace("network",cur_net)
        
        # current configuration
        self.cur_config=cur_config
        self.store_conf()
        #self.get_model()

    def get_model(self):
        """This is a function for establishing remote connection
        """
        try:
            key=paramiko.RSAKey.from_private_key_file(self.keyfile)
            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self.host, username=self.user, password=self.passwd, 
                               pkey=key)
            #stdin, stdout, stderr=ssh_client.exec_command("python /home/tester/FlexiBO/models/xception.py")
        
            ftp_client=ssh_client.open_sftp()
            ftp_client.get("/home/tester/model.h5","/home/nvidia/model.h5")
            ftp_client.close()
        except:
            traceback.print_exc()
            print ("[ERROR]: could not ssh")

    def store_conf(self):
        """This function is used to store current configuration to yaml
        """
        conf=dict(cur_conf=self.cur_config)
        with open ("cur_config.yaml","w", ) as curfp:
            yaml.dump(conf, curfp, default_flow_style=False)
ConfigNetwork("xception", [16,3,16,16,16])
    
with open ("cur_config.yaml","r") as pfp:
    pfg=yaml.load(pfp)

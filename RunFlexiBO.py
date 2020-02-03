import sys
import os
from optparse import OptionParser
import pandas as pd

def config_option_parser():
    """This function is used to configure option parser 
    @returns:
        options: option parser handle
    """
    usage="""USAGE: %python RunFlexiBO.py -m [mode] -d [data] -s [surrogate]
             online: python RunFlexiBO.py -m online -d measurements.csv -s GP
             offline: python RunFlexiBO.py -m offline -d measurements.csv -s RF
            
    """
    parser=OptionParser(usage=usage)
    parser.add_option('-m', "--mode",
                      action="store",
                      type="string",
                      dest="mode",
                      help="mode")
    parser.add_option('-d', "--data",
                      action="store",
                      type="string",
                      dest="data",
                      help="rows")
    parser.add_option('-s', "--surrogate",
                      action="store",
                      type="string",
                      dest="surrogate",
                      help="surrogate")
    (options,args)=parser.parse_args()
    return (options, usage)

if __name__=="__main__":
    options, _=config_option_parser()
    data=pd.read_csv(os.path.join(os.getcwd(),options.data))
    if options.mode=="online":
        from src.flexibo_online import FlexiBO
        bo=FlexiBO(data, options.surrogate)
    elif options.mode=="offline":
        from src.flexibo_offline import FlexiBO
        bo=FlexiBO(data, options.surrogate)
    else:
        print ("[ERROR]: Invalid Mode")


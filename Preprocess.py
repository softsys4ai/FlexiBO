from __future__ import division
import os
import pandas as pd 

def normalize(col):
    """This function is used to nortmalize a column 
    Args: 
        col name of the axis which is to be normalize
    """
    maximum=df[col].max()
    minimum=df[col].min()
    for index,row in df.iterrows():
        df.ix[index,col]=(row[col]-minimum)/(maximum-minimum)
    

if __name__=="__main__":
    fname="data.csv"
    global df
    df=pd.read_csv(os.path.join(os.getcwd(),fname))
    df=df[['number_of_cores',
          'core_freq',
          'gpu_freq',
          'emc_freq',
          'inference_time',
          'power_consumption']]
    cols=list(df.columns)
    for col in cols:
        if col == 'inference_time':
            continue
        elif col == 'power_consumption':
            continue 
        else:
            normalize(col)
    df.to_csv("proc.csv")
    

import sys
import os
import pandas as pd
from src.flexibo import FlexiBO



if __name__=="__main__":
    fname="data.csv"
    data=pd.read_csv(os.path.join(os.getcwd(),fname))
    bo=FlexiBO(data)

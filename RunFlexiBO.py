import sys
import pandas as pd
from src.flexibo import FlexiBO

if __name__=="__main__":
    mode = sys.argv[1]
    bo=FlexiBO(mode)

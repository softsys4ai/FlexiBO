import pandas as pd
from src.FlexiBO import FlexiBO

df=pd.read_csv('./data/Input/it_ec_te_obj.csv')
bo=FlexiBO(df)

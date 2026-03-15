""" 
Collect and replicate anomalies data.

====================
Author: Zhaogang(Tony) Huang
Date: March 2026
"""

#%% Initialize
#| ### Create output folders
import datetime, os, time, sys
import matplotlib
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy 
import tensorflow
import pandas_datareader

datapath = 'data/Anomalies/17NOV21/NYSE/monthly/'

respath = 'test/'
figpath = respath + 'figures/'
tblpath = respath + 'tables/'
os.makedirs(figpath, exist_ok=True)
os.makedirs(tblpath, exist_ok=True)
print(f'output folders: {respath}')

#| ### System timer helper function
reset = False
timeit_t0 = time.time()
def timeit(reset=False):
    global timeit_t0
    if reset:
        timeit_t0 = time.time()
    else:
        print('{:7.2f}s elapsed.'.format(time.time() - timeit_t0))

#%% Load data
#| ### anomalies names
with open('anom_names.txt', 'r') as f:
    anom_names = eval(f.read())

#| ### combine data
def load_anomaly_data(anom):
    global tblpath, datapath

    try:
        frames = []
        for var in ['ret', 'dp_div', 'n']:
            df         = pd.read_csv(datapath + f"{var}3_{anom}.csv", index_col=0)
            df.index   = pd.to_datetime(df.index, format='mixed') + pd.offsets.MonthEnd(0)
            df.columns = [f"{c}_{var}" for c in df.columns]

            frames.append(df)

        data = pd.concat(frames, axis=1)
        data.index = pd.MultiIndex.from_arrays(
            [[anom] * len(data), data.index],
            names=['anomaly', 'date']
        )
        data.to_csv(tblpath + f"{anom}.csv")
        print(f"{anom:<10} √")

    except:
        print(f"Error loading data for anomaly '{anom}'.")

for anom, exp in anom_names.items():
    load_anomaly_data(anom)

# %% Combine data
# python3 -m pip install tensorflow -i https://pypi.tuna.tsinghua.edu.cn/simple
import pandas as pd
import numpy as np
import os
from pathlib import Path

df = pd.read_csv('C:/Users/davil/Desktop/test_sample.csv')

print(df)

def cond_df(x: object):
	if 'K' in x:
		x = x.str.replace('K')
		x = float(x) * 1000
		return x
	elif 'M' in x:
		x = x.str.replace('M')
		x = float(x) * 1000000
		return x
	else:
		return x


df['newcash'] = df.apply(cond_df, axis = 1)

print(df)
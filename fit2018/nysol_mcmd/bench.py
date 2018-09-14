#!/usr/bin/env python
# -*- coding: utf-8 -*-/
import os
import sys
import time
from pprint import pprint
from datetime import datetime
from glob import glob

import pandas as pd
import math
import nysol.mcmd as nm

loop=5

iPath=root="./DATA"
oPath=root="./OUTPUT/bench"
os.system("mkdir -p %s"%(oPath))
oFile="%s/price_%d.txt"%(oPath,loop)

t={'id':'str','date':'int','o':'float','h':'float','l':'float','c':'float'}

def pd1(iFile):
	df = pd.read_csv(iFile)
	dfg=df.groupby("date")
	r = dfg.mean(numeric_only = True)

def nm1(iFile):
	r = nm.mhashsum(k="date",f="o,h,l,c",i=iFile).run()

def nm1a(iPath):
	fs=[]
	for iFile in glob("%s/*"%iPath):
		fs.append(nm.mhashsum(f="o,h,l,c",i=iFile))
	r=nm.runs(fs)

def pd2(iFile):
	df=pd.read_csv(iFile,dtype=t,usecols=['id','date','c'])
	df_id=df.groupby("id", sort=False).apply(lambda x: x.sort_values(["date"])).reset_index(drop=True)
	r=df_id.groupby("id", sort=False).rolling(on="date",window=3, min_periods=3).mean()

def nm2(iFile):
	f=None
	f <<= nm.mcut(f="id,date,c",i=iFile)
	f <<= nm.mwindow(k="id",wk="date:win",t=3)
	f <<= nm.mavg(k="id,win",f="c")
	f <<= nm.writelist(dtype="win:int,date:int,c:float")
	r=f.run()

def nm2a(iFile):
	f=None
	f <<= nm.mcut(f="id,date,c",i=iFile)
	f <<= nm.mwindow(k="id",wk="date:win",t=3)
	f <<= nm.mavg(k="id,win",f="c",o="%s/output_nm2.csv"%oPath)
	r=f.run()


def pd3(iFile):
	df = pd.read_csv(iFile,dtype=t)
	dfo = df.o.iloc; dfh = df.h.iloc
	dfl = df.l.iloc; dfc = df.c.iloc
	r=[0.0,0.0,0.0,0.0]
	for idx in range(df.shape[0]):
		r[0]+=dfo[idx] if not math.isnan(dfo[idx]) else 0.0
		r[1]+=dfh[idx] if not math.isnan(dfh[idx]) else 0.0
		r[2]+=dfl[idx] if not math.isnan(dfl[idx]) else 0.0
		r[3]+=dfc[idx] if not math.isnan(dfc[idx]) else 0.0

def pd3a(iFile):
	df = pd.read_csv(iFile,dtype=t)
	dfo = df.o.values; dfh = df.h.values
	dfl = df.l.values; dfc = df.c.values
	r=[0.0,0.0,0.0,0.0]
	for idx in range(df.shape[0]):
		r[0]+=dfo[idx] if not math.isnan(dfo[idx]) else 0.0
		r[1]+=dfh[idx] if not math.isnan(dfh[idx]) else 0.0
		r[2]+=dfl[idx] if not math.isnan(dfl[idx]) else 0.0
		r[3]+=dfc[idx] if not math.isnan(dfc[idx]) else 0.0

def nm3(iFile):
	r=[0.0,0.0,0.0,0.0]
	for line in nm.mnullto(f="*",v=0,i=iFile).convtype(t):
		r[0]+= line[2];r[1]+= line[3]
		r[2]+= line[4];r[3]+= line[5]

sec={}
mean={}
params=[]
small ="%s/price_small.csv"%iPath
middle="%s/price_middle.csv"%iPath
large ="%s/price_large.csv"%iPath

params.append(["pd1" ,small])
params.append(["nm1" ,small])
params.append(["pd2" ,small])
params.append(["nm2" ,small])
params.append(["nm2a",small])
params.append(["pd3" ,small])
params.append(["pd3a",small])
params.append(["nm3" ,small])
params.append(["pd1" ,middle])
params.append(["nm1" ,middle])
params.append(["pd2" ,middle])
params.append(["nm2" ,middle])
params.append(["nm2a",middle])
params.append(["pd3" ,middle])
params.append(["pd3a",middle])
params.append(["nm3" ,middle])

params.append(["pd1" ,large])
params.append(["nm1" ,large])
params.append(["nm1a","%s/sep"%iPath])
params.append(["pd2" ,large])
params.append(["nm2" ,large])
params.append(["nm2a",large])
#params.append(["pd3" ,large])
params.append(["pd3a",large])
params.append(["nm3" ,large])

for param in params:
	func=param[0]
	iFile=param[1]
	name="%s_%s"%(func,iFile)
	print("START:",name)
	sec[name]=[]
	for i in range(loop):
		st=time.time()
		eval(func+'("%s")'%iFile)
		sec[name].append(time.time()-st)
		print("loop",i,time.time()-st)
	mean[name]=0
	for i in range(loop):
		mean[name]+=sec[name][i]
	mean[name]/=loop

print("write to: ",oFile)
with open(oFile, "w") as file:
	pprint(sys.argv[0], stream=file)
	pprint(loop, stream=file)
	pprint(sec, stream=file)
	pprint(mean, stream=file)


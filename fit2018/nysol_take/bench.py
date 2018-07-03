#!/usr/bin/env python
# -*- coding: utf-8 -*-/
import os
import sys
import time
from pprint import pprint

from nysol.take.extcore import lcm
import Orange
from orangecontrib.associate.fpgrowth import *

loop=5

iPath=root="./DATA"
oPath=root="./OUTPUTS/bench"
os.system("mkdir -p %s"%(oPath))
oFile="%s/bench_%d.txt"%(oPath,loop)

def L1(iFile,minFreq):
	lcm(type="Ff",sup=minFreq,i=iFile,o="xxrsl11")

def O1(iFile,minFreq):
	tbl = Orange.data.Table(iFile)
	X, mapping = OneHot.encode(tbl)
	itemsets =frequent_itemsets(X, minFreq)

sec={}
mean={}
params=[]

params.append(["L1" ,   1,"%s/onlineT_all.csv"%iPath])
params.append(["O1" ,   1,"%s/onlineO_all.basket"%iPath])
params.append(["L1" ,  10,"%s/onlineT_size10.csv"%iPath])
params.append(["O1" ,  10,"%s/onlineO_size10.basket"%iPath])
params.append(["L1" , 100,"%s/onlineT_size100.csv"%iPath])
params.append(["O1" , 100,"%s/onlineO_size100.basket"%iPath])
params.append(["L1" ,1000,"%s/onlineT_size1000.csv"%iPath])
params.append(["O1" ,1000,"%s/onlineO_size1000.basket"%iPath])

for param in params:
	func   =param[0]
	size   =param[1]
	iFile  =param[2]
	minFreq=size*100
	name="%s_%d"%(func,size)
	print("START:",name)
	sec[name]=[]
	for i in range(loop):
		st=time.time()
		eval(func+'("%s",%d)'%(iFile,minFreq))
		sec[name].append(time.time()-st)
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


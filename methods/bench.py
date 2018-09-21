#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import time
from pprint import pprint
from datetime import datetime
from glob import glob
import nysol.mcmd as nm


def mcut(iFile,loop):
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.mcut(f="id,key1,key2,key3,int1,int2,float1,float2,date,time",i=iFile,o="oFile").run()
		sec.append(time.time()-st)
	return sec

def msortf_key1(iFile,loop):
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.msortf(f="key1",i=iFile,o="oFile").run()
		sec.append(time.time()-st)
	return sec

def msortf_key2(iFile,loop):
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.msortf(f="key1",i=iFile,o="oFile").run()
		sec.append(time.time()-st)
	return sec

def msortf_key3(iFile,loop):
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.msortf(f="key1",i=iFile,o="oFile").run()
		sec.append(time.time()-st)
	return sec

def msortf_float2(iFile,loop):
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.msortf(f="float2%n",i=iFile,o="oFile").run()
		sec.append(time.time()-st)
	return sec

def msum_key3(iFile,loop):
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.msum(k="key3",f="int1,int2,float1,float2",i=iFile,o="oFile").run()
		sec.append(time.time()-st)
	return sec

def msum_key3_presort(iFile,loop):
	nm.msortf(f="key3",i=iFile,o="sorted").run()
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.msum(k="key3",f="int1,int2,float1,float2",i="sorted",o="oFile").run()
		sec.append(time.time()-st)
	return sec


def mhashsum_key3(iFile,loop):
	sec=[]
	for i in range(loop):
		st=time.time()
		nm.mhashsum(k="key3",f="int1,int2,float1,float2",i=iFile,o="oFile").run()
		sec.append(time.time()-st)
	return sec

def cal(sec):
	mean=0
	for s in sec:
		mean+=s
	mean/=len(sec)
	sd=0
	for s in sec:
		sd+=(s-mean)**2
	sd/=(len(sec)-1)
	sd=sd**(1/2)
	return mean,sd

iPath="./rand"
loop=5
small =10000
middle=1000000
large =100000000
funcs=[]
funcs.append("mcut")
funcs.append("msum_key3")
funcs.append("msum_key3_presort")
funcs.append("mhashsum_key3")
#funcs.append("msortf_key1")
#funcs.append("msortf_key2")
funcs.append("msortf_key3")
funcs.append("msortf_float2")

with open("methods.csv","w") as fpw:
	fpw.write("method,dataSize,mean,sd\n")
	for func in funcs:
		for size in [tiny,small]:
		#for size in ["small","middle","large","huge"]:
			iFile="%s/%d.csv"%(iPath,size)
			name="%s_%s"%(func,size)
			print("START:",name)
			sec=eval(func+'("%s",%d)'%(iFile,loop))
			print("tm",sec)
			mean,sd=cal(sec)
			fpw.write("%s,%s,%f,%f\n"%(func,size,mean,sd))

os.system("cat methods.csv")


#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import time
import datetime
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


##########################################################################
# functions for benchmark test
##########################################################################
# calculate actual execution time for each method
# iFile
# method,dataSize,mean,sd
# mcut,10000,0.004002,0.000703
# mcut,1000000,0.307001,0.001781
# oFile
# method,small,middle,large
# mcut,0.004002(0.000703),0.307001(0.001781),30.737572(0.125166)
# msum_key3,0.087729(0.113214),1.494672(0.012172),190.174376(1.948978)
# msum_key3_presort,0.014930(0.000098),0.463388(0.001697),35.182463(0.048672)
def calTime(iFile,oFile):
	f=None
	f <<= nm.mnumber(q=True, a="id", i=iFile)
	f <<= nm.mcal(c='$s{mean}+"("+$s{sd}+")"', a="time")
	f <<= nm.m2cross(k="method",s="dataSize",f="time")
	f <<= nm.msortf(f="id%n")
	f <<= nm.mcut(f="method,10000:small,1000000:middle,100000000:large")
	f <<= nm.mfldname(q=True,o=oFile)
	f.run()

# calculate relative execution time to "mcut" method for each method
# iFile
# method,dataSize,mean,sd
# mcut,10000,0.004002,0.000703
# mcut,1000000,0.307001,0.001781
# oFile
# mcut,1,1,1
# msum_key3,21.9,4.9,6.2
# msum_key3_presort,3.7,1.5,1.1
# mhashsum_key3,7.4,2.6,1.8
def calRelative(iFile,oFile):
	mcut=None
	mcut <<= nm.mselstr(f="method",v="mcut", i="methods.csv")

	f=None
	f <<= nm.mnumber(q=True, a="id", i=iFile)
	f <<= nm.mjoin(k="dataSize",m=mcut,f="mean:base")
	f <<= nm.mcal(c='round(${mean}/${base},0.1)', a="score")
	f <<= nm.m2cross(k="method",s="dataSize",f="score")
	f <<= nm.msortf(f="id%n")
	f <<= nm.mcut(f="method,10000:small,1000000:middle,100000000:large")
	f <<= nm.mfldname(q=True,o=oFile)
	f.run()

# calculate mean and SD of multiple executions
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

################
# entry point

iPath="./DATA"
loop=5
small =10000
middle=1000000
large =100000000
funcs=[]
funcs.append("mcut")
funcs.append("msum_key3")
funcs.append("msum_key3_presort")
funcs.append("mhashsum_key3")
funcs.append("msortf_key3")
funcs.append("msortf_float2")

with open("methods.csv","w") as fpw:
	fpw.write("method,dataSize,mean,sd\n")
	for func in funcs:
		for size in [small,middle,large]:
			iFile="%s/%d.csv"%(iPath,size)
			name="%s_%s"%(func,size)
			print("START:",name)
			sec=eval(func+'("%s",%d)'%(iFile,loop))
			print("tm",sec)
			mean,sd=cal(sec)
			fpw.write("%s,%s,%f,%f\n"%(func,size,mean,sd))

today = datetime.date.today().strftime('%Y%m%d')
calTime("methods.csv","time_%s.csv"%today)
calRelative("methods.csv","score_%s.csv"%today)

os.system("output files: methods.csv, time.csv, score.csv")


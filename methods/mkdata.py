#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import nysol.mcmd as nm

# generate random data
# id,key1,key2,key3,int1,int2,float1,float2,date,time
def mkdata(rowSize,oFile):
	f=None
	f <<= nm.mnewnumber(a="id", l=rowSize)
	f <<= nm.mrand(min=0   ,max=9     ,int=True,S=1111,a="key1")
	f <<= nm.mrand(min=100 ,max=999   ,int=True,S=1113,a="key2")
	f <<= nm.mrand(min=10000,max=99999,int=True,S=1117,a="key3")
	f <<= nm.mcal(c='randi(0,999,101)',   a="int1")
	f <<= nm.mcal(c='randi(-999,999,111)',a="int2")
	f <<= nm.mcal(c='rand(991)',          a="float1")
	f <<= nm.mcal(c='rand(997)*200-100',  a="float2")
	f <<= nm.mcal(c='0d20100101+randi(0,3650,137)',    a="date")
	f <<= nm.mcal(c='right(t2s(0t000000+randi(0,86399,133)),6)', a="time", o=oFile)
	f.run()

oPath="./rand/"
os.system("mkdir -p %s"%oPath)

for size in [10000,1000000,100000000]:
	mkdata(size, "%s/%s.csv"%(oPath,size))


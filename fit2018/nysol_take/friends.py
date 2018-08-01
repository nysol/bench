#!/usr/bin/env python
# -*- coding: utf-8 -*-/
import os
import sys
import networkx as nx

import matplotlib
matplotlib.use('Agg') # 追加
import matplotlib.pyplot as plt

import nysol.mcmd as nm
import nysol.take as nt
from nysol.util.margs import Margs
##### 上の2行は、以下に置き換え
##### import nysol.take as nt

iFile=("./DATA/online_all.csv")
oPath=("./OUTPUT/friends")
os.system("mkdir -p %s"%oPath)

# Make a similarity graph of StockCode: frequent 2-itemset enumeration

# iFile
# InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
# 536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,2010/12/1 8:26,2.55,17850,United Kingdom
# 536365,71053,WHITE METAL LANTERN,6,2010/12/1 8:26,3.39,17850,United Kingdom
f=None
f <<= nm.mcut(f="InvoiceNo,StockCode",i=iFile)
f <<= nm.muniq(k="InvoiceNo,StockCode",o="%s/tra.csv"%oPath)
f.run(msg="on")

#args=Margs(["dummy","S=100","tid=InvoiceNo","item=StockCode","i=%s/tra.csv"%oPath,"O=%s"%oPath,"l=2","u=2"],"i=,x=,O=,tid=,item=,class=,taxo=,type=,s=,S=,sx=,Sx=,g=,p=,-uniform,l=,u=,top=,T=,-replaceTaxo")
#mitemset(args).run()
##### 上の2行は、以下で動くようにする
nt.mitemset(S=100,tid="InvoiceNo",item="StockCode",l=2,u=2,i="%s/tra.csv"%oPath,O=oPath).run()

# patterns.csv
# pid,size,count,total,support%0nr,lift,pattern
# 86,2,833,25900,0.03216216216,8.209,22386 85099B
# 501,2,784,25900,0.03027027027,17.1523,22697 22699
# 129,2,733,25900,0.0283011583,7.4039,21931 85099B

# Filitering the friend pairs of StockCode in the similarity graph of StockCode.
f=None
f <<= nm.msplit(f="pattern",a="item1,item2",i="%s/patterns.csv"%oPath)
f <<= nm.mcut(f="item1,item2,lift",o="%s/rules.csv"%oPath)
f.run(msg="on")

#os.system("mfriends.rb ef=item1,item2 ei=%s/rules.csv ef=item1,item2 sim=lift rank=5 eo=%s/friends.csv -udout"%(oPath,oPath))
##### 上の行は、以下で動くようにする
nt.mfriends(ef="item1,item2",ei="%s/rules.csv"%oPath,sim="lift", rank=5, udout=True, eo="%s/friends.csv"%oPath).run()

# visualization of the graph
f=None
f <<= nm.mcal(c="cat(\" \",$s{item1},$s{item2})", a="edges", i="%s/friends.csv"%oPath)
f <<= nm.mcut(f="edges",nfno=True,o="%s/edges.csv"%oPath)
f.run(msg="on")

G = nx.read_edgelist("%s/edges.csv"%oPath)
pos=nx.spring_layout(G)
plt.figure(figsize=(10, 10))
nx.draw(G, pos=pos,node_size=40,iterations=20)

plt.savefig("%s/friends.png"%oPath)


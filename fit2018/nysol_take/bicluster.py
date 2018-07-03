#!/usr/bin/env python
# -*- coding: utf-8 -*-/
import os
import sys
import nysol.mod as nm
##### import nysol.mcmd as nm

iFile=("./DATA/online_all.csv")
oPath=("./OUTPUT/bicluster")
os.system("mkdir -p %s"%oPath)

# make a bipartitle graph of StockCode-CustomerID
f=None
f <<= nm.mcut(f="StockCode,CustomerID",i=iFile)
f <<= nm.mdelnull(f="StockCode,CustomerID")
f <<= nm.mcount(k="StockCode,CustomerID",a="freq")
f <<= nm.mselnum(f="freq",c='[5,]',o="%s/bipartiteGraph.csv"%oPath)
f.run()

# biclusterig on the bipartite graph non-polished
os.system("mbiclique.rb ei=%s/bipartiteGraph.csv ef=StockCode,CustomerID o=%s/clique_non-polish.csv"%(oPath,oPath))
##### 上の行を下で置き換える
##### nt.mbiclique(ei="%s/bipartiteGraph.csv"%oPath, ef="StockCode,CustomerID", o="%s/clique_non-polish.csv"%oPath).run()

# biclusterig on the bipartite graph polished
os.system("mbipolish.rb ei=%s/bipartiteGraph.csv ef=StockCode,CustomerID sim=R th=0.3 eo=%s/bipartiteGraphPolish.csv"%(oPath,oPath))
os.system("mbiclique.rb ei=%s/bipartiteGraphPolish.csv ef=StockCode,CustomerID o=%s/clique_polish.csv"%(oPath,oPath))
##### 上の2行を下2行で置き換える
##### nt.mbipolish(ei="%s/bipartiteGraph.csv"%oPath, ef="StockCode,CustomerID", sim="R", th=0.3, eo="%s/bipartiteGraphPolish.csv"%oPath).run( )
##### nt.mbiclique(ei="%s/bipartiteGraphPolish.csv"%oPath,ef="StockCode,CustomerID", o=”%s/clique_polish.csv"%oPath).run()

# histogram by cluster size of CustomerID (non-polish)
f=None
f <<= nm.mchgnum(f="size2",R="1,3,5,7,9,11,21,31,41,51,MAX",v="1-2,3-4,5-6,7-8,9-10,11-20,21-30,31-40,41-50,51-",i="%s/clique_non-polish.csv"%oPath)
f <<= nm.mcut(f="size2")
f <<= nm.mcount(k="size2",a="freq",o="%s/hist_non-polish.csv"%oPath)
f.run(meg="on")

# histogram by cluster size of CustomerID (polish)
f=None
f <<= nm.mchgnum(f="size2",R="1,3,5,7,9,11,21,31,41,51,MAX",v="1-2,3-4,5-6,7-8,9-10,11-20,21-30,31-40,41-50,51-",i="%s/clique_polish.csv"%oPath)
f <<= nm.mcut(f="size2")
f <<= nm.mcount(k="size2",a="freq",o="%s/hist_polish.csv"%oPath)
f.run(meg="on")


#!/usr/bin/env python
# -*- coding: utf-8 -*-/estimation.csv 
import os
import nysol.mcmd as nm

os.environ["KG_VerboseLevel"]="3"
debug="on"

iPath="./DATA"
oPath="./OUTPUT/apriori"
os.system("mkdir -p %s"%oPath)

iFile="%s/price_large.csv"%(iPath)
topix="%s/index.csv"%(iPath)

# make a transaction data, which date as a transaction and tickerID as an item
tra=None
tra <<= nm.mcut(f="id,date,c",i=iFile)
tra <<= nm.mjoin(k="date",m=topix,f="i")
tra <<= nm.mslide(k="id",s="date",f="date:date2,c:c2,i:i2")
tra <<= nm.mcal(c="${c2}/${c}-${i2}/${i}",a="ret")
tra <<= nm.mselnum(f="ret",c="[0.05,0.1]")
tra <<= nm.mcut(f="id,date2:date,ret")

# frequency of one item
freq=None
freq <<= nm.mcut(f="id",i=tra)
freq <<= nm.mcount(k="id",a="freq")
freq <<= nm.mselnum(f="freq",c="[5,]")

# total number of transactions
total=None
total <<= nm.mcut(f="date",i=tra)
total <<= nm.muniq(k="date")
total <<= nm.mcount(a="total")

# frequency of cooccurence of id, and calculate lift values
itemCoFreq=None
itemCoFreq <<= nm.mcut(f="date,id",i=tra)
itemCoFreq <<= nm.mcommon(k="id",m=freq)
itemCoFreq <<= nm.mcombi(k="date",n=2,f="id",a="id1,id2")
itemCoFreq <<= nm.mcut(f="id1,id2")
itemCoFreq <<= nm.mfsort(f="id1,id2")
itemCoFreq <<= nm.mcount(k="id1,id2",a="coFreq")
itemCoFreq <<= nm.mjoin(k="id1",m=freq,K="id",f="freq:freq1")
itemCoFreq <<= nm.mjoin(k="id2",m=freq,K="id",f="freq:freq2")
itemCoFreq <<= nm.mproduct(m=total,f="total")
itemCoFreq <<= nm.mcal(c="(${coFreq}*${total})/(${freq1}*${freq2})",a="lift")
itemCoFreq <<= nm.msel(c="${lift}>10 && ${coFreq}>6")
r=itemCoFreq.run(msg=debug)
print(r)
print(len(r))

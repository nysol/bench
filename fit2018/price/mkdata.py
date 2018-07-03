#!/usr/bin/env python
# -*- coding: utf-8 -*-/
import os
import sys
from datetime import datetime,timedelta
import numpy as np
import nysol.mod as nm

def mkData(oFile):
	np.random.seed(seed=32)
	startDate=datetime(2018, 6, 29)
	delta=timedelta(days=1)

	with open(oFile,"w") as fpw:
		fpw.write("id,date,o,h,l,c\n")
		for id in range(1000,7000):
			period=int(np.random.normal(4600,2000))
			if period<1000:
				period=1000
			print("id",id,"period",period)
			date=startDate
			c=np.random.randint(500,100000)
			for days in range(period):
				if c<10:
					break
				c=np.random.normal(1.00,0.02)*c
				o=np.random.normal(1.00,0.02)*c
				h=np.random.normal(1.04,0.02)*c
				l=np.random.normal(0.96,0.02)*c
				hh=max(c,o,h,l)
				ll=min(c,o,h,l)
				h=hh
				l=ll
				date=date-delta
				fpw.write("%d,%s,%d,%d,%d,%d\n"%(id,date.strftime("%Y%m%d"),o,h,l,c))

mkData("./DATA/price_large.csv")
nm.mselnum(f="date",c="[20171225,]",i="./DATA/price_large.csv",o="./DATA/price_middle.csv").run()
nm.mselnum(f="date",c="[20180610,]",i="./DATA/price_middle.csv",o="./DATA/price_small.csv").run()
nm.msep(d="./DATA/sep/${date}", p=True, i="./DATA/price_large.csv").run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-/estimation.csv 
import os
import xlrd
from numpy.random import *
from datetime import datetime,timedelta
import urllib.request
import nysol.mod as nm

debug="on"
datPath="./DATA"
os.system("mkdir -p %s"%datPath)

def download():
	print("downloading original dataset...")
	url="http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
	urllib.request.urlretrieve(url, "%s/onlineRetail.xlsx"%datPath)

def xlsx2tsv():
	print("reading xlsx...")
	oFile = "%s/onlineRetail.tsv"%datPath
	book  = xlrd.open_workbook("%s/onlineRetail.xlsx"%datPath)
	sheet = book.sheet_by_name('Online Retail')
	# 8 cols x 541910 rows
	# InvoiceNo       StockCode       Description     Quantity        InvoiceDate     UnitPrice       CustomerID      Country
	# 536365  85123A  WHITE HANGING HEART T-LIGHT HOLDER      6       2010/12/1 8:26  2.55    17850   United Kingdom
	# 536365  71053   WHITE METAL LANTERN     6       2010/12/1 8:26  3.39    17850   United Kingdom
	# 536365  84406B  CREAM CUPID HEARTS COAT HANGER  8       2010/12/1 8:26  2.75    17850   United Kingdom

	print("writing xlsx as tsv...")
	with open(oFile,"w") as fpw:
		for row in range(541910):
			line=[]
			for col in range(8):
				cell=sheet.cell(row, col)
				if cell.ctype == xlrd.XL_CELL_NUMBER:  # number
					val = cell.value
					if val.is_integer(): # remove .0
						val = int(val)

				elif cell.ctype == xlrd.XL_CELL_DATE:  # date
					val=(datetime(1899, 12, 30) + timedelta(days=cell.value)).strftime("%Y%m%d")
				else:
					val = cell.value

				line.append(str(val))
			fpw.writelines(("\t".join(line))+"\n")

def mkCSV():
	# InvoiceNo       StockCode       Description     Quantity        InvoiceDate     UnitPrice       CustomerID      Country
	# 536365  85123A  WHITE HANGING HEART T-LIGHT HOLDER      6       2010/12/1 8:26  2.55    17850   United Kingdom
	# 536365  71053   WHITE METAL LANTERN     6       2010/12/1 8:26  3.39    17850   United Kingdom
	# 536365  84406B  CREAM CUPID HEARTS COAT HANGER  8       2010/12/1 8:26  2.75    17850   United Kingdom
	iFile="%s/onlineRetail.tsv"%(datPath)

	f=None
	f<<= nm.mtab2csv(i=iFile,o="%s/online_all.csv"%datPath)
	f.run(msg=debug)

def toNum():
	for size in ["all"]:
		iFile="%s/online_all.csv"%datPath
		oFile1="%s/onlineT_all.csv"%datPath     # data for Take.core
		oFile2="%s/onlineO_all.basket"%datPath  # data for Orange
		oFile3="%s/onlineM_all.csv"%datPath     # data for Take

		f=None
		f <<= nm.mcut(f="InvoiceNo,StockCode",i=iFile)
		f <<= nm.muniq(k="InvoiceNo,StockCode")
		f <<= nm.mfldname(q=True,o=oFile3)
		f.run(msg=debug)

		st=None
		st <<= nm.mcut(f="StockCode",i=iFile)
		st <<= nm.muniq(k="StockCode")
		st <<= nm.mnumber(s="StockCode",a="num")
		f=None
		f <<= nm.mjoin(k="StockCode",m=st,f="num",i=iFile)
		f <<= nm.mcut(f="InvoiceNo,num:StockCode")
		f <<= nm.mtra(k="InvoiceNo",f="StockCode")
		f <<= nm.mcut(f="StockCode",nfno=True,o=oFile1)
		f.run(msg=debug)

		os.system("tr ' ' ',' <%s >%s"%(oFile1,oFile2))

def jitter(items):
	size=len(items)
	for pos in list(set(binomial(n=size-1, p=0.3, size=size))):
		items[pos]=str(randint(4070))
	return list(set(items))

def enlarge(scale):
	print("START enlarge",scale)

	# data for Take.core
	iFile="%s/onlineT_all.csv"%datPath
	oFile="%s/onlineT_size%d.csv"%(datPath,scale)
	with open(oFile,"w") as fpw:
		for i in range(scale):
			for line in nm.mcut(f=0,nfni=True,i=iFile):
				if i==0:
					fpw.write(line[0]+"\n")
				else:
					items=line[0].split(" ")
					newItems=jitter(items)
					fpw.write(" ".join(newItems)+"\n")
		
	# data for Orange
	iFile="%s/onlineT_size%d.csv"%(datPath,scale)
	oFile="%s/onlineO_size%d.basket"%(datPath,scale)
	os.system("tr ' ' ',' <%s >%s"%(iFile,oFile))
	return


download()
xlsx2tsv()

mkCSV()
toNum()

enlarge(10)
enlarge(100)
enlarge(1000)


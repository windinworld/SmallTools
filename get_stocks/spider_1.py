#!/usr/bin/env python
#-*- coding: utf-8 -*-
from urllib import urlopen
from pprint import pprint
import re,os,math

stocks = ('上证指数','中国联通','浙江龙盛','浦发银行','青岛啤酒','唐山港','中国人寿','中国银行','金隅股份','万科A','怡亚通')
stocks_num = [0,3000,200,500,200,700,200,2000,900,300,100]

def get_stock_info(stocks):
    stock_info = {}
    i = 0
    for stock in stocks:
        url = "http://www.baidu.com/s?tn=baidu&wd="+stock
        #url = "http://www.sogou.com/web?query="+stock
        webpage = urlopen(url)
        text = webpage.read()
        m = re.search('"display":{"cur":{"num":"([.\d]+)","status":"(\w+)","info":"[-+][.\d]+\s+\(([+-][.\d]+%)\)',text)
        #stock_info[stock] = {'price':m.group(1)}
        stock_info[stock] = {}
        stock_info[stock]['price'] = m.group(1)
        stock_info[stock]['status'] = m.group(2)
        stock_info[stock]['increase'] = m.group(3)
        price = stocks_num[i]* float(stock_info[stock]['price'])
        stock_info[stock]['my_price'] = price
        i+=1
#        print "stock:%-20s price:%-10s my_price:%-10s status:%-10s percentage:%-10s" % (stock,stock_info[stock]['price'],price,stock_info[stock]['status'],stock_info[stock]['increase'])
    return stock_info

def output_stock_stat(stock_info):
    total_price = 0
    for stock in stock_info.iterkeys():
         stock_info[stock]
         print "stock:%-20s price:%-10s my_price:%-10s status:%-10s percentage:%-10s" % (stock,stock_info[stock]['price'],stock_info[stock]['my_price'],stock_info[stock]['status'],stock_info[stock]['increase'])
         total_price += stock_info[stock]['my_price']
    h_price = 105776
    print "total price: %f" % total_price
    print "history price: %f" %h_price
    h_per = (total_price-h_price)/h_price*100.0
    h_increase = total_price-h_price
    print "history increase: %f %%" %h_per
    print "history increase value: %f " %h_increase
    if abs(h_per) > 1.5:
         os.system("echo %.3f,%f,%f|mail -s 'stock alert %.3f' ningbaofeng126@126.com" %(h_per,total_price,h_increase,h_per))
stock_info = get_stock_info(stocks)
output_stock_stat(stock_info)


#    total_price += stocks_num[i]* float(num)

#print "total price: %f" % total_price
#print "history price: %f" %h_price
#h_per = (total_price-h_price)/h_price*100.0
#print "history increase: %f " %h_per,"%"
#if abs(h_per) > 1.5:
#   os.system("echo %.3f,%f|mail -s 'stock alert %.3f' ningbaofeng126@126.com" %(h_per,total_price,h_per))


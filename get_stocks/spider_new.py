#!/usr/bin/env python
#-*- coding: utf-8 -*-
#import httplib2
import urllib
import httplib
import urllib2
from pprint import pprint
import re,os,math,json
import logging
from time import sleep
from time import asctime
from ConfigParser import ConfigParser
CONFIGFILE =  "stocks.cfg"

logging.basicConfig(level=logging.INFO,filename='stocks.log')
cur_time = asctime()
logging.info('Starting program: %s' % cur_time)






#stocks = ('上证指数','中国联通','浙江龙盛','浦发银行','唐山港','中国人寿','中国银行','金隅股份','万科A','怡亚通')
stocks = ('上证指数','中国联通','浙江龙盛','浦发银行','唐山港','中国人寿','中国银行','金隅股份','万科A')
#stocks_id = ('sh000001','sh600050','sh600352','sh600000','sh601000','sh601628','sh601988','sh601992','sz000002','sz002183')
#stocks_id = ('sh000001','sh600050','sh600352','sh600000','sh601000','sh601628','sh601988','sh601992','sz000002','sz002415')
config = ConfigParser()
config.read(CONFIGFILE)
stocks_id = config.get('stocks','stocks_id').split(',')
#stocks_num = [0,3000,400,500,700,200,2000,900,300,100]
stocks_num = [0,4000,700,900,100,600,220]
#stocks_in = [0,9.3,33.2,17.1,15.5,38.5,4.48,12.87,13.91,57.35]
stocks_in = [0,9.3,15.5,12.87,46.5,57,40]
#stocks_out = [0,12,40,20,18,45,5.5,15,20,90,100]
stocks_out = [0,12,18,15,20,50,50]

def api_baidu_stock(stock_id):
    url = "apis.baidu.com"
    uri = "/apistore/stockservice/stock?stockid="+stock_id
    #url = "http://apis.baidu.com/apistore/stockservice/stock?stockid="
    #url += stock_id
#    headers = {'apikey':'3dcaf4331db97fac7b478f2eca0665e2'}
#    req = urllib2.Request(url=url,headers=headers)
#    req.add_header('apikey','3dcaf4331db97fac7b478f2eca0665e2')
#    print req.get_header('apikey'.capitalize())
    conn = httplib.HTTPConnection(url)
    headers = {'apikey':'3dcaf4331db97fac7b478f2eca0665e2'}
    conn.request("GET",uri,headers = headers)
    #response = urllib2.urlopen(req)
    response = conn.getresponse()
    page = response.read()
    conn.close()
    #print(page.decode("utf8"))
    return page
def api_sina_stock(stock_id):
    url =  "http://hq.sinajs.cn/list="+stock_id
    req = urllib.urlopen(url)
    page = req.read()
    page = page.decode("gbk")    
#    page = page.encode("utf8")    
#    var hq_str_sh000001="上证指数,4943.742,4941.714,4970.485,4970.485,4906.815,0,0,237882247,383263189991,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2015-05-28,10:27:33,00";
    m = re.search('var hq_str_\w+=\"(.+[.\w]+)\"',page)
    return m.group(1)
def get_stock_info(stocks_id):
    stock_info = {}
    i = 0
    for stock_id in stocks_id:
        """ 
        ###Begin Baidu API
        text =api_baidu_stock(stock_id)
        sleep(0.3)
        decode_json = json.loads(text)
        
        #init stock info 
        currentPrice = decode_json['retData']['stockinfo']['currentPrice']
        hPrice = decode_json['retData']['stockinfo']['hPrice']
        lPrice = decode_json['retData']['stockinfo']['lPrice']
        OpenningPrice =  decode_json['retData']['stockinfo']['OpenningPrice']
        closingPrice = decode_json['retData']['stockinfo']['closingPrice']
        time = decode_json['retData']['stockinfo']['time']
        name = decode_json['retData']['stockinfo']['name']
        date = decode_json['retData']['stockinfo']['date']
        ###END Baidu API
        """
        text = api_sina_stock(stock_id)
        sina_stock = text.split(',')
        currentPrice = float(sina_stock[3])
        hPrice = float(sina_stock[4])
        lPrice = float(sina_stock[5])
        OpenningPrice = float(sina_stock[1])
        closingPrice = float(sina_stock[2])
        time = sina_stock[31]
        name = sina_stock[0]
        date = sina_stock[30]
        stock_info[stock_id] = {}
        stock_info[stock_id]['my_number'] = stocks_num[i]
        stock_info[stock_id]['my_input'] = stocks_in[i]
        stock_info[stock_id]['my_output'] = stocks_out[i]     

        stock_info[stock_id]['currentPrice'] = currentPrice
        stock_info[stock_id]['hPrice'] = hPrice
        stock_info[stock_id]['lPrice'] = lPrice
        stock_info[stock_id]['OpenningPrice'] = OpenningPrice
        stock_info[stock_id]['closingPrice'] = closingPrice
        stock_info[stock_id]['time'] = time
        stock_info[stock_id]['name'] = name
        stock_info[stock_id]['date'] = date
        stock_info[stock_id]['my_price'] = currentPrice * stocks_num[i]
	if currentPrice >= closingPrice: 
	    status = 'up'
	else:
	    status = 'down'
        stock_info[stock_id]['status'] = status
        increase_p = float("%.2f" % ((currentPrice-closingPrice)/closingPrice*100) )
        increase_v = float("%.2f" % (currentPrice-closingPrice) )
        stock_info[stock_id]['increase_p'] = increase_p
        stock_info[stock_id]['increase_v'] = increase_v
	
        

        """
        m = re.search('"display":{"cur":{"num":"([.\d]+)","status":"(\w+)","info":"[-+][.\d]+\s+\(([+-][.\d]+%)\)',text)
        #stock_info[stock] = {'price':m.group(1)}
        stock_info[stock] = {}
        stock_info[stock]['price'] = m.group(1)
        stock_info[stock]['status'] = m.group(2)
        stock_info[stock]['increase'] = m.group(3)
        price = stocks_num[i]* float(stock_info[stock]['price'])
        stock_info[stock]['my_price'] = price
        """
        i+=1
    return stock_info

def output_stock_stat(stocks_id):
    total_price = 0
    #for stock_id in stock_info.iterkeys():
    for stock_id in stocks_id:
         format = "stock_id:%-15s stock_name:%-15s price:%-10s my_price:%-10s status:%-10s percentage:  %10s%%"
         print format % (stock_id,stock_info[stock_id]['name'],stock_info[stock_id]['currentPrice'],stock_info[stock_id]['my_price'],stock_info[stock_id]['status'],stock_info[stock_id]['increase_p'])
         total_price += stock_info[stock_id]['my_price']
    h_price = 120000
    print "total price: %f" % total_price
    print "threshold price: %f" %h_price
    h_per = (total_price-h_price)/h_price*100.0
    h_increase = total_price-h_price
    print "history increase: %f %%" %h_per
    print "history increase value: %f " %h_increase
    if abs(h_per) > 2:
         os.system("echo %.3f,%f,%f|mail -s 'stock alert %.3f' ningbaofeng126@126.com" %(h_per,total_price,h_increase,h_per))

#api_baidu_info("sh600050")
def threadhold_check(stocks_id):
    decrease_threshold = 3
    increase_threshold = 10
    for stock_id in stocks_id:
        if stock_info[stock_id]['my_input'] == 0: continue
	t_increase  = stock_info[stock_id]['currentPrice'] - stock_info[stock_id]['my_input']
        t_increase_per = float("%.2f" %((t_increase / stock_info[stock_id]['my_input'])*100))
        my_gain = t_increase*stock_info[stock_id]['my_number']
        diff = float("%.2f" %((stock_info[stock_id]['my_output']- stock_info[stock_id]['currentPrice'])/stock_info[stock_id]['currentPrice']*100))
        format = "stock_name:%-15s percentage:%10.2f%% gains:%-10.2f output_diff:%5.2f%%"
        print format % (stock_info[stock_id]['name'],t_increase_per,my_gain,diff)
        
        if t_increase_per < 0 and abs(t_increase_per)>decrease_threshold:
             print "decrease>%d%% %s" %(decrease_threshold,stock_info[stock_id]['name'])
        elif t_increase_per > increase_threshold:
	    print "increase>%d%% %s" %(increase_threshold,stock_info[stock_id]['name'])
#        diff = float("%.2f" %((stock_info[stock_id]['my_output']- stock_info[stock_id]['currentPrice'])/stock_info[stock_id]['currentPrice']*100))
#        print "Distant rate to selling: %-10s %.2f%%" %(stock_info[stock_id]['name'],diff) 
        
        
stock_info = get_stock_info(stocks_id)
output_stock_stat(stock_info)
#threadhold_check(stocks_id)


#    total_price += stocks_num[i]* float(num)

#print "total price: %f" % total_price
#print "history price: %f" %h_price
#h_per = (total_price-h_price)/h_price*100.0
#print "history increase: %f " %h_per,"%"
#if abs(h_per) > 1.5:
#   os.system("echo %.3f,%f|mail -s 'stock alert %.3f' ningbaofeng126@126.com" %(h_per,total_price,h_per))


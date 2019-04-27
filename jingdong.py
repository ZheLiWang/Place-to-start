# coding:utf-8
from lxml import etree
import sys
import time
from multiprocessing.dummy import Pool as Threadpool
import requests
import json
from pymongo import MongoClient
import datetime
import pymysql

import importlib
import sys
importlib.reload(sys)

def get_sku_id(url):
    html= requests.get(url,headers = headers)
    selector = etree.HTML(html.text)
    product_list = selector.xpath('//*[@id="J_goodsList"]/ul/li')
    for product in product_list:
        product_sku = product.xpath("@data-sku")[0]
        get_phont_content(product_sku)
        get_phone_price(product_sku)


def get_phont_content(sku):
    content_url = 'https://item.jd.com/{}.html'.format(sku)
    html = requests.get(content_url)
    selector = etree.HTML(html.text)
    product_detail = selector.xpath('//ul[@class="parameter2 p-parameter-list"]')
    for product_li in product_detail:
        product_dict["手机名称"] = product_li.xpath("li[1]/@title")[0]
        product_dict["手机编号"] = product_li.xpath("li[2]/@title")[0]
        product_dict["手机产地"] = product_li.xpath("li[4]/@title")[0]


def get_phone_price(sku):
    phone_url = 'https://p.3.cn/prices/mgets?callback=jQuery1346298&type=1&area=1_72_2799_0&pdtk=&pduid=1713961549&pdpin=&pin=null&pdbp=0&skuIds=J_{}'.format(str(sku))
    phone_detail = requests.get(phone_url,headers = headers).content
    ss = phone_detail.decode('utf-8')
    ss = ss.split("(")[1]
    ss = ss.split(")")[0]
    phone_json = json.loads(ss)
    for info in phone_json:
        product_dict["手机价格"] = info.get("p")
    save_mysql(product_dict)



def save_mysql(product_dict):
	db = pymysql.connect(host="localhost",user="root",passwd="123456",db="python_wzl",charset="utf8")
	cursor = db.cursor()
	sql = "insert into jingdong(name,phoneno,address,price) values(%s,%s,%s,%f)"%("'"+product_dict["手机名称"]+"'","'"+product_dict["手机编号"]+"'","'"+product_dict["手机产地"]+"'",float(product_dict["手机价格"]))
	print(sql)
	cursor.execute(sql)
	db.commit()

product_dict = {}
i = 1111


if __name__ == '__main__':
    #save_mysql()
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    html = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&page={}'.format(page) for page in range(1,10)]
    #html = get_sku_id('https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8'  )
    pool = Threadpool(2)
    pool.map(get_sku_id,html)
    pool.close()
    pool.join()
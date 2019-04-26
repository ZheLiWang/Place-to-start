# -*- coding: utf-8 -*-
from django.shortcuts import render
from jd import models
import MySQLdb



def get_data(sql):#获取数据库的数据
    conn = MySQLdb.connect('127.0.0.1','root','123456','python_wzl',port=3306)   
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall() 
    cur.close()
    conn.close()
    return results

def order(request):# 向页面输出订单
    sql = "select * from jingdong" 
    m_data = get_data(sql)
    return render(request,'index.html',{'order':m_data})
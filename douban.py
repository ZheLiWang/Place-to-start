import requests
from bs4 import BeautifulSoup

import pymysql
 
 
def get_pages_link():
    # 插入到数据库
    db = pymysql.connect(host="localhost",user="root",passwd="123456",db="python_wzl",charset="utf8")
    cursor = db.cursor()
 
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        'Connection': 'keep-alive'
    }
 
    for item in range(0, 250, 25):
        url = "https://movie.douban.com/top250?start={}".format(item)
        web_data = requests.get(url, headers=header)
        soup = BeautifulSoup(web_data.content, 'lxml')
        for movie in soup.select('#wrapper li'):
 
            #href = movie.select('.hd > a')[0]  # 链接
            href=movie.find('a')["href"]
            name = movie.select('.hd > a > span')[0].text  # 片名
            star = movie.select('.rating_num')[0].text  # 评分
            people = movie.select('.star > span')[3].text  # 评价人数
            try:
                quote = movie.select('.inq')[0].text
            except:
                print('没有quote哦')
                quote = None
            data = {
                # 'url': href,
                '评分': star,
                '片名': name,
                '名言': quote,
                '评价人数': people
            }
            sql = "insert into douban(score,name,quote,people) values ('%f','%s','%s','%s')"%(float(star), name, quote, people)
            cursor = db.cursor()
            print(sql)
            cursor.execute(sql)
            db.commit()
 
            print(data)
            # print(movie)
        print('\n' + '-' * 50 + '\n')
    # 关闭数据库
    cursor.close()
    conn.close
 
 
if __name__ == '__main__':
    get_pages_link()
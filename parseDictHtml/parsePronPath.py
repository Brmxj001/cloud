import MySQLdb as mysql
import time
from bs4 import BeautifulSoup as soup

db  = mysql.connect("localhost","root", "admin", "dict", charset="utf8" )

cursor  = db.cursor()

cursor.execute("select version()")

data = cursor.fetchone()

print(data)


#parse file
source = open("/Users/wangxiaobo/brmxj/mysql/source.html")
start = time.time()
soup = soup(source)

opentime = time.time()
results = soup.find_all(class_="entry_content")
i = 0
def intoMysql(title, href):
    try:
        sql = "update word set pron_path='{pron_path}' where name = '{name}'".format(pron_path=href, name=title)
        print("执行的sql语句是:",sql)
        cursor.execute(sql)        
        print("执行完毕")
        db.commit()
        print("执行完毕")
    except Exception as e:
        db.rollback()
        print("fail")
        print(repr(e))
for result in results:
    # 获取发音
    pronounce = result.find(class_="PronCodes")
    title = result.find(class_="pagetitle")
    if title is None:
        continue
    if pronounce is None:
        continue
    if not "href" in pronounce.attrs:
        continue

    print(type(pronounce.attrs))
    title = title.text
    print("pron is:", pronounce)
    print(type(pronounce))
    print(type(pronounce['href']))
    if pronounce is not None:
        href = pronounce['href'].split('sound:/')[1]
        print("title is : ", title)
        print("href is ",href)
        intoMysql(title, href)
        print("__________________________________________")
end = time.time()
print("执行时间",end-start)
print("打开文件的时间,",opentime-start)
db.close()


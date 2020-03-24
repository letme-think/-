import pymysql
import re, urllib.request

count = 0
url = "https://so.gushiwen.org/shiwenv"
poetry_Tang_url = "https://so.gushiwen.org/gushi/shijing.aspx"

# 唐诗链接
def get_links(url1):
    html = urllib.request.urlopen(url1).read()
    html = html.decode("UTF-8")
    reg = r'<a href="/shiwenv(.*?)" target'
    urls = re.findall(reg, html)
    chapter_url = []
    for a in urls:
        chapter_url.append(url + a)
    return chapter_url

# 唐诗正文内容
def get_poem_content(url2):
    html = urllib.request.urlopen(url2).read()
    html = html.decode("UTF-8")
    res = '<h1 style="font-size:.*?;">(.*?)</h1>\n<p class="source"><a href=".*?">(.*?)</a>.*?<a href=".*?">(.*?)</a> </p>\n<div class="contson" id="contson.*?">\n([\s\S]*?)\n</div>'
    poem_content = re.compile(res).findall(html)
    return poem_content

def conn_mysql():
    url = '127.0.0.1'
    username = 'root'
    password = '123456'
    dbname = 'graduateproject01'
    db = pymysql.connect(url, username, password, dbname)
    return db

def createtable_poem():
    sql = 'create table if not exists Shijing(poem_name varchar(50),author_name varchar(50),dynasty varchar(50),content text)'
    db = conn_mysql()
    db.cursor().execute(sql)
    db.commit()

if __name__ == '__main__':
    db = conn_mysql()
    createtable_poem()
    poem_name = []
    a = len(get_links(poetry_Tang_url))
    print(a)
    j = 0
    for i in get_links(poetry_Tang_url):
        while j < a:
            b = get_links(poetry_Tang_url)[j]
            poem_content = get_poem_content(b)
            pl = poem_content[0]
            sql = 'insert into Shijing(poem_name,author_name,dynasty,content) values (%s,%s,%s,%s)'
            data = [pl[0], pl[2], pl[1], re.sub('<br />|<p>|</p>', '', pl[3])]
            db.cursor().execute(sql, data)
            db.commit()
            j += 1





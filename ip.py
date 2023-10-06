import requests
from bs4 import BeautifulSoup
from psycopg2._psycopg import IntegrityError
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#蜜蜂代理网站的免费ip
def get_page(start,end):

    headers={
        'User - Agent':
            'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 117.0.0.0Safari / 537.36Edg / 117.0.2045.55'
    }
    for page_number in range(start, end + 1):
        url = f"https://www.beesproxy.com/free/page/{page_number}"
        print(f'第{page_number}页')
        response=requests.get(url=url,headers=headers)
        content=response.text

        soup=BeautifulSoup(content,'html.parser')
        tr_all=soup.find('table',class_='table table-bordered bg--secondary').find('tbody').find_all('tr')
        for tr in tr_all:
            ip=tr.find_all('td')[0].get_text()
            port = tr.find_all('td')[1].get_text()
            location = tr.find_all('td')[2].get_text()
            print(ip,port,location)
            try:
                # 创建数据模型对象并插入到数据库
                new_article = IPInfo(
                    ip_address=ip,
                    port = port,
                    location=location
                )
                session.add(new_article)
                session.commit()
                # print("URL:", url)
                # print("Title:", title)
                # print("Content:", content)
                # 确保其他字段也正确打印


            except :
                session.rollback()  # 回滚当前事务，取消已插入的数据
                # 可以在这里记录日志，报告问题，或者采取其他措施
                continue  # 跳过当前数据，继续处理下一个数据`
if __name__ == '__main__':
    start_page = 3
    end_page=20

    db_url = 'postgresql://postgres:1078769434@127.0.0.1:5432/postgres'

    engine = create_engine(db_url)
    connection = engine.connect()
    # 创建数据模型
    Base = declarative_base()

    class IPInfo(Base):
        __tablename__ = 'ip_location'

        id = Column(Integer, primary_key=True)
        ip_address = Column(String(15), unique=True, nullable=False)
        port = Column(Integer)
        location = Column(String(255))


    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    get_page(start_page, end_page)

    # 关闭会话
    session.close()




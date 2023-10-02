from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError

db_url = 'postgresql://wH2020:Rcts3We0xdo9@82.157.251.34:5065/wendeng'
engine = create_engine(db_url)
connection = engine.connect()
# 创建数据模型
Base = declarative_base()

class Open_Government(Base):
    __tablename__ = 'open_government'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    content = Column(Text)
    maketime = Column(String)
    description = Column(String)
    columnname = Column(String)
    keywords = Column(String)
    sitedomain = Column(String)

# 创建数据库会话
Session = sessionmaker(bind=engine)
session = Session()

departments_2 = {
    '政务公开': {},
    # 添加更多部门...
}

driver = webdriver.Chrome()

def get_page_data( start_page, end_page, departments):
    for page_number in range(start_page, end_page + 1):
        url = f"http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={page_number}&pg=20&cateid=1141&tpl=1361&checkError=1"
        # 发送请求并获取页面内容
        driver.get(url)
        time.sleep(2)
        print(f'第{page_number}页')
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        div_tags = soup.find_all('div', class_='jcse-news-url')

        for div in div_tags:
            a_tags = div.find_all('a')

            for a in a_tags:
                link = a.string
                print("Link:", link)  # 添加这行打印语句
                if 'http://www.wendeng.gov.cn/col' in link:
                    continue
                driver.get(link)
                time.sleep(1)
                try:
                    wait = WebDriverWait(driver, 2)
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.art_con')))
                    new_content = driver.page_source
                    new_soup = BeautifulSoup(new_content, 'html.parser')
                except:
                    continue

                # 提取页面数据
                page_data = {
                    'url': [],
                    'Titles': [],
                    'Maketime': [],
                    'description': [],
                    'ColumnName': [],
                    'keywords': [],
                    'SiteDomain': [],
                    'art_con_texts': [],
                }

                meta_tags = new_soup.find_all('meta')

                for meta in meta_tags:
                    if 'name' in meta.attrs and 'content' in meta.attrs:
                        name_value = meta['name']
                        content_value = meta['content']

                        if name_value == 'url':
                            page_data['url'].append(content_value)
                        elif name_value == 'ArticleTitle':
                            page_data['Titles'].append(content_value)
                        elif name_value == 'Maketime':
                            page_data['Maketime'].append(content_value)
                        elif name_value == 'description':
                            page_data['description'].append(content_value)
                        elif name_value == 'ColumnName':
                            page_data['ColumnName'].append(content_value)
                        elif name_value == 'keywords':
                            page_data['keywords'].append(content_value)
                        elif name_value == 'SiteDomain':
                            page_data['SiteDomain'].append(content_value)

                art_con_texts = []

                for tr in new_soup.find_all('tr'):
                    try:
                        td = tr.find('td', class_='bt_content')
                        if td:
                            div = td.find('div', class_='art_con')
                            if div:
                                p_tags = div.find_all('p')
                                # texts = [p.get_text(strip=True) for p in p_tags]
                                texts = [p.get_text().replace(" ", "").replace("\n", "") for p in p_tags]

                                art_con_texts.extend(texts)
                    except Exception as e:
                        print('Error:', e)  # 打印异常信息

                page_data['art_con_texts'] = art_con_texts

                if '政务公开' not in departments:
                    departments_2['政务公开'] = []

                departments_2['政务公开'].append(page_data)
                # 遍历字典中的页面数据
                for category, page_data_list in departments_2.items():
                    for page_data in page_data_list:
                        # 从字典中提取关键信息
                        try:
                            url = page_data['url'][0]
                            title = page_data['Titles'][0]
                            content = '\n'.join(page_data['art_con_texts'])
                            maketime = page_data['Maketime'][0]
                            description = page_data['description']
                            columnname = page_data['ColumnName'][0]
                            keywords = page_data['keywords'][0]
                            sitedomain = page_data['SiteDomain'][0]

                            # 创建数据模型对象并插入到数据库
                            new_article = Open_Government(
                                url=url,
                                title=title,
                                content=content,
                                maketime=maketime,
                                description=description,
                                columnname=columnname,
                                keywords=keywords,
                                sitedomain=sitedomain
                            )
                            # print("URL:", url)
                            # print("Title:", title)
                            # print("Content:", content)
                            # 确保其他字段也正确打印
                        except:
                            continue
                    try:
                        session.add(new_article)
                        session.commit()
                    except IntegrityError:
                        session.rollback()  # 回滚当前事务，取消已插入的数据
                        # 可以在这里记录日志，报告问题，或者采取其他措施
                        continue  # 跳过当前数据，继续处理下一个数据

start_page = 145
# 开始页
end_page = 832    # 结束页
departments_2 = {}  # 初始化departments字典
get_page_data( start_page, end_page, departments_2)

#打印部门字典中的数据
for department, data in departments_2.items():
    print(department + ':')
    if department == '政务公开':
        for page_data in data:
            print('\tPage Data:')
            for category, values in page_data.items():
                print('\t\t', category + ':', values)
    else:
        for category, values in data.items():
            print('\t', category + ':', values)





# # 创建数据库表
# Base.metadata.create_all(engine)





# 关闭数据库会话
session.close()
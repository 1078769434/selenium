from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ARRAY, Boolean, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError

db_url = 'postgresql://wH2020:Rcts3We0xdo9@82.157.251.34:5065/wendeng'
engine = create_engine(db_url)
connection = engine.connect()
# 创建数据模型
Base = declarative_base()

class WebPage(Base):
    __tablename__ = "web_page"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    published = Column(DateTime, nullable=False)
    description = Column(String(512), nullable=True)
    category = Column(String(64), nullable=False)
    keywords = Column(ARRAY(String(64)), nullable=True)
    content = Column(String, nullable=True)
    site_domain = Column(String(64), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())
    weight = Column(Integer, nullable=False, default=0)
    crawl_at = Column(DateTime, nullable=False, default=func.now())

# 创建数据库会话
Session = sessionmaker(bind=engine)
session = Session()


driver = webdriver.Chrome()
departments_2 = {
    '政务公开': {},
    # 添加更多部门...
}
def get_page_data( start_page, end_page, departments):
    for page_number in range(start_page, end_page + 1):
        url = f"http://www.wendeng.gov.cn/col/col79327/index.html?uid=299353&pageNum={page_number}"
        # 发送请求并获取页面内容
        driver.get(url)
        time.sleep(2)
        print(f'第{page_number}页')
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        # 查找具有class为'default_pgContainer'的div
        div_element = soup.find('div', class_='default_pgContainer')


        ul_element = div_element.find('ul')



        li_elements = ul_element.find_all('li')

        # 遍历li元素并获取a标签的href属性
        for li in li_elements:
            a_element = li.find('a')
            href = a_element.get('href')
            link = href
            if  '/art/' in link:
                print("Link:", link)  # 添加这行打印语句
                driver.get('http://www.wendeng.gov.cn/'+link)
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
                    'ColumnType': [],
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
                        elif name_value == 'ColumnType':
                            page_data['ColumnType'].append(content_value)
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
                            columnname = page_data['ColumnType'][0]
                            keywords = page_data['keywords'][0]
                            sitedomain = page_data['SiteDomain'][0]

                            # 创建数据模型对象并插入到数据库
                            new_article = WebPage(
                                url=url,#网址
                                title=title,#标题
                                # content=content,
                                published=maketime,#发布时间
                                description=description,#摘要
                                category=columnname,#分类
                                keywords=keywords,#关键词
                                site_domain=sitedomain#域名
                            )
                            session.add(new_article)
                            session.commit()
                            # print("URL:", url)
                            # print("Title:", title)
                            # print("Content:", content)
                            # 确保其他字段也正确打印


                        except IntegrityError:
                            session.rollback()  # 回滚当前事务，取消已插入的数据
                            # 可以在这里记录日志，报告问题，或者采取其他措施
                            continue  # 跳过当前数据，继续处理下一个数据
            else:
                continue
start_page = 1
# 开始页
end_page = 4    # 结束页
departments_2 = {}  # 初始化departments字典
get_page_data( start_page, end_page, departments_2)







# # 创建数据库表
# Base.metadata.create_all(engine)





# 关闭数据库会话
session.close()
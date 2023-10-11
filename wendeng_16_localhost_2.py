from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ARRAY, Boolean, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError

db_url = ''#数据库连接
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


# 创建ChromeOptions对象，并配置为无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')  # 启用无头模式
chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速

# 创建Chrome浏览器实例
driver = webdriver.Chrome(options=chrome_options)
departments_2 = {
    '政务公开': {},
    # 添加更多部门...
}

def get_page_data( start_page, end_page, departments):

    for page_number in range(start_page, end_page + 1):
        try:
            #要闻
            #781页
            # 记录开始时间
            start_time = time.time()

            url = f"http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={page_number}&pg=20&cateid=1082&tpl=1361&checkError=1"
            # 发送请求并获取页面内容
            driver.get(url)
            time.sleep(0.5)
            print(f'第{page_number}页')
            content = driver.page_source
            soup = BeautifulSoup(content, 'lxml')



            div_tags = soup.find_all('div', class_='jcse-news-url')

            for div in div_tags:
                a_tags = div.find_all('a')

                for a in a_tags:
                    link = a.string
                    # if 'http://www.wendeng.gov.cn/' not in link:
                    #     continue
                    print("Link:", link)  # 添加这行打印语句

                    driver.get(link)
                    time.sleep(0.5)
                    try:
                        wait = WebDriverWait(driver, 1)
                        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.art_con')))
                        new_content = driver.page_source
                        new_soup = BeautifulSoup(new_content, 'lxml')
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
                                page_data['keywords'].append(content_value.replace(' ', '').replace(',', '').replace(',',''))
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
                                content = '\n'.join(page_data['art_con_texts']).replace(' ', '').replace('\n', '')
                                maketime = page_data['Maketime'][0]
                                description = page_data['description']
                                columnname = page_data['ColumnType'][0]
                                keywords = page_data['keywords'][0].replace(' ', '').replace(',', '').replace('，','').replace('\n','')
                                sitedomain = page_data['SiteDomain'][0]

                                # 创建数据模型对象并插入到数据库
                                new_article = WebPage(
                                    url=url,#网址
                                    title=title,#标题
                                    content=content,#页面内容
                                    published=maketime,#发布时间
                                    description=str(description),#摘要
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
                                # print(time.time())

                            except IntegrityError:
                                session.rollback()  # 回滚当前事务，取消已插入的数据
                                # 可以在这里记录日志，报告问题，或者采取其他措施
                                continue  # 跳过当前数据，继续处理下一个数据
        except:
            continue
        # 记录结束时间
        end_time = time.time()
        # 计算爬取一条数据所需的时间（秒）
        elapsed_time = end_time - start_time

        print(f"爬取一条数据所需的时间: {elapsed_time} 秒")

start_page = 27  #83页  #这个脚本300页之后到781页的爬过
# 开始页
end_page = 781   # 结束页
departments_2 = {}  # 初始化departments字典
get_page_data( start_page, end_page, departments_2)







# # 创建数据库表
# Base.metadata.create_all(engine)





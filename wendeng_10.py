from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_15(url, p, departments):
    # 要闻    #780页
    # 替换以下参数为实际的数据库连接信息
    # db_url = 'postgresql://wH2020:Rcts3We0xdo9@82.157.251.34:5065/wendeng'
    # engine = create_engine(db_url)
    # connection = engine.connect()

    if p < 2:   #设置爬取页数 递归爬取
        # 创建浏览器对象
        driver = webdriver.Chrome()

        # 发送请求并获取页面内容
        driver.get(url)

        # 等待页面加载完毕，最多等待5秒
        time.sleep(5)

        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')

        div_tags = soup.find_all('div', class_='jcse-news-url')
        for div in div_tags:
            a_tags = div.find_all('a')

            for a in a_tags:
                link = a.string
                print("Link:", link)  # 添加这行打印语句

                driver.get(link)
                wait = WebDriverWait(driver, 10)  # 最长等待时间为 10 秒
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.art_con')))
                new_content = driver.page_source
                new_soup = BeautifulSoup(new_content, 'html.parser')

                # 提取<meta>标签的content值
                meta_tags = new_soup.find_all('meta')
                # 创建一个小字典，用于存储页面数据
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
                # 提取<div>标签中所有<p>标签中的文本并去除空格
                art_con_texts = []
                for tr in new_soup.find_all('tr'):
                    try:
                        td = tr.find('td', class_='bt_content')
                        if td:
                            div = td.find('div', class_='art_con')
                            if div:
                                p_tags = div.find_all('p')
                                texts = [p.get_text(strip=True) for p in p_tags]
                                art_con_texts.extend(texts)
                    except Exception as e:
                        print('Error:', e)  # 打印异常信息

                # 将文本添加到departments字典中
                page_data['art_con_texts'] = art_con_texts  # 文章内容
                if '资讯中心' not in departments:
                    departments['资讯中心'] = []  # 创建一个列表用于存储page_data

                # 添加page_data到'资讯中心'键对应的值，而不是覆盖
                departments['资讯中心'].append(page_data)

                # 打印部门字典中的数据
                for department, data in departments.items():
                    print(department + ':')
                    if department == '资讯中心':
                        for page_data in data:
                            print('\tPage Data:')
                            for category, values in page_data.items():
                                print('\t\t', category + ':', values)
                    else:
                        for category, values in data.items():
                            print('\t', category + ':', values)
        p += 1
        new_url = f'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={p}&pg=20&cateid=1082&tpl=1361&checkError=1'
        driver.quit()
        return get_15(new_url, p, departments)

url_2 = 'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p=1&pg=20&cateid=1082&tpl=1361&checkError=1'
departments = {}  # 初始化departments字典
get_15(url_2, 1, departments)

print(departments)







departments_3 = {
    '政务服务': []  # 创建一个空列表用于存储各个页面的数据
}


def get_3(url, p, departments_3):
    # 政务服务
    if p < 2:
        driver = webdriver.Chrome()

        # 发送请求并获取页面内容
        driver.get(url)

        # 等待页面加载完毕，最多等待5秒
        time.sleep(5)

        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')

        div_tags = soup.find_all('div', class_='jcse-news-title')
        for div in div_tags:
            a_tags = div.find('a')
            span_tags = div.find_all('span')

            # 遍历每个<a>标签
            for a in a_tags:
                title = a.get_text().strip()
                page_data = {'title': title, 'categorize': '', 'content': ''}

            for span in span_tags:
                categorize = span.get_text().strip()
                page_data['categorize'] = categorize

            # 提取表格数据
            table_tags = soup.find('table').find('tbody').find_all('tr')

            content_list = []  # 用于存储所有行的content数据

            for table in table_tags:
                content_tags = table.find_all('td')
                content = [content.get_text().strip() for content in content_tags]
                content_list.append(content)  # 将content数据追加到列表

            # 将整个content_list存储到page_data中
            page_data['content'] = content_list

            # 将每个页面数据添加到政务服务列表
            departments_3['政务服务'].append(page_data)

        p += 1
        new_url = f'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={p}&pg=20&cateid=1103&tpl=1361&checkError=1'
        driver.quit()  # 关闭当前页面的浏览器实例，避免资源泄漏

        return get_3(new_url, p, departments_3)


url = 'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p=1&pg=20&cateid=1103&tpl=1361&checkError=1'
# get_3(url, 1, departments_3)

# 打印departments_3大字典
# print(departments_3)



departments_2 = {
                    '政务公开': {


                    }

                    # 添加更多部门...
                }



def get_16(url, p, departments):
    #  政府信息公开    #792页
    # 替换以下参数为实际的数据库连接信息
    # db_url = 'postgresql://wH2020:Rcts3We0xdo9@82.157.251.34:5065/wendeng'
    # engine = create_engine(db_url)
    # connection = engine.connect()

    if p < 3:
        # 创建浏览器对象
        driver = webdriver.Chrome()

        # 发送请求并获取页面内容
        driver.get(url)

        # 等待页面加载完毕，最多等待5秒
        time.sleep(5)

        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')

        div_tags = soup.find_all('div', class_='jcse-news-url')
        for div in div_tags:
            a_tags = div.find_all('a')

            for a in a_tags:
                link = a.string
                print("Link:", link)  # 添加这行打印语句

                driver.get(link)
                time.sleep(3)
                wait = WebDriverWait(driver, 10)  # 最长等待时间为 10 秒
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.art_con')))
                new_content = driver.page_source
                new_soup = BeautifulSoup(new_content, 'html.parser')

                # 提取<meta>标签的content值
                meta_tags = new_soup.find_all('meta')
                # 创建一个小字典，用于存储页面数据
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
                # 提取<div>标签中所有<p>标签中的文本并去除空格
                art_con_texts = []
                for tr in new_soup.find_all('tr'):
                    try:
                        td = tr.find('td', class_='bt_content')
                        if td:
                            div = td.find('div', class_='art_con')
                            if div:
                                p_tags = div.find_all('p')
                                texts = [p.get_text(strip=True) for p in p_tags]
                                art_con_texts.extend(texts)
                    except Exception as e:
                        print('Error:', e)  # 打印异常信息

                # 将文本添加到departments字典中
                page_data['art_con_texts'] = art_con_texts  # 文章内容
                if '政务公开' not in departments:
                    departments['政务公开'] = []  # 创建一个列表用于存储page_data

                # 添加page_data到'资讯中心'键对应的值，而不是覆盖
                departments['政务公开'].append(page_data)

                # 打印部门字典中的数据
                for department, data in departments.items():
                    print(department + ':')
                    if department == '政务公开':
                        for page_data in data:
                            print('\tPage Data:')
                            for category, values in page_data.items():
                                print('\t\t', category + ':', values)
                    else:
                        for category, values in data.items():
                            print('\t', category + ':', values)
        p += 1
        new_url = f'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={p}&pg=20&cateid=1141&tpl=1361&checkError=1'

        return get_16(new_url, p, departments)

url_3 = 'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p=1&pg=20&cateid=1141&tpl=1361&checkError=1'
departments_2 = {}  # 初始化departments字典
# get_16(url_3, 1, departments_2)

# print(departments_2)


departments_4 = {
    "政民互动":{

    }


}

def get_15(url, p, departments):
    # 政民互动    #780页
    # 替换以下参数为实际的数据库连接信息
    # db_url = 'postgresql://wH2020:Rcts3We0xdo9@82.157.251.34:5065/wendeng'
    # engine = create_engine(db_url)
    # connection = engine.connect()

    if p < 2:
        # 创建浏览器对象
        driver = webdriver.Chrome()

        # 发送请求并获取页面内容
        driver.get(url)

        # 等待页面加载完毕，最多等待5秒
        time.sleep(5)

        content = driver.page_source

        soup = BeautifulSoup(content, 'html.parser')

        div_tags = soup.find_all('div', class_='jcse-news-url')
        for div in div_tags:
            a_tags = div.find_all('a')

            for a in a_tags:
                link = a.string
                print("Link:", link)  # 添加这行打印语句
                if 'http://tyjspt.weihai.gov.cn/jact/front' in link:
                    continue

                driver.get(link)
                wait = WebDriverWait(driver, 10)  # 最长等待时间为 10 秒
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.art_con')))
                new_content = driver.page_source
                new_soup = BeautifulSoup(new_content, 'html.parser')

                # 提取<meta>标签的content值
                meta_tags = new_soup.find_all('meta')
                # 创建一个小字典，用于存储页面数据
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
                # 提取<div>标签中所有<p>标签中的文本并去除空格
                art_con_texts = []

                # 此处应该使用new_soup，而不是soup
                div = new_soup.find('div', class_='art_con')

                if div:
                    p_tags = div.find_all('p')
                    texts = [p.get_text(strip=True) for p in p_tags]
                    art_con_texts.extend(texts)

                # 将文本添加到departments字典中
                page_data['art_con_texts'] = art_con_texts  # 文章内容
                if '政民互动' not in departments:
                    departments['政民互动'] = []  # 创建一个列表用于存储page_data

                # 添加page_data到'资讯中心'键对应的值，而不是覆盖
                departments['政民互动'].append(page_data)

                # 打印部门字典中的数据
                for department, data in departments.items():
                    print(department + ':')
                    if department == '政民互动':
                        for page_data in data:
                            print('\tPage Data:')
                            for category, values in page_data.items():
                                print('\t\t', category + ':', values)
                    else:
                        for category, values in data.items():
                            print('\t', category + ':', values)
        p += 1
        new_url = f'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={p}&pg=20&cateid=1161&tpl=1361&checkError=1'

        return get_15(new_url, p, departments)

url_2 = 'http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p=1&pg=20&cateid=1161&tpl=1361&checkError=1'
departments = {}  # 初始化departments字典
# get_15(url_2, 1, departments_4)

# print(departments_4)
import scrapy
from bs4 import BeautifulSoup

from wendeng.items import WendengItem

import pdb

class WendengSpiderSpider(scrapy.Spider):
    name = "wendeng_spider"
    allowed_domains = ["www.wendeng.gov.cn"]
    # start_urls = ["http://www.wendeng.gov.cn/index.html"]
    def start_requests(self):
        for page_number in range(1, 2):
            yield scrapy.Request(f"http://www.wendeng.gov.cn/col/col140376/index.html?uid=299353&pageNum={page_number}")


    def parse(self, response):
        # 使用Beautiful Soup来解析HTML内容
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        ul = soup.find('div', class_='rsx_cont').find('ul')
        # 设置断点
        # pdb.set_trace()
        li = ul.find_all('li')
        for li_tag in li:
            a = li_tag.find('a')
            href = a.get('href')
            link = 'http://www.wendeng.gov.cn' + href
            yield scrapy.Request(link, callback=self.parse_detail)
    def parse_detail(self, response):
        new_soup = BeautifulSoup(response.text,'lxml')
        meta_tags = new_soup.find_all('meta')
        item = WendengItem()








        for meta in meta_tags:
            if 'name' in meta.attrs and 'content' in meta.attrs:
                name_value = meta['name']
                content_value = meta['content']

                if name_value == 'url':
                    item['url'] = content_value
                elif name_value == 'ArticleTitle':
                    item['title'] = content_value
                elif name_value == 'PubDate':
                    item['published'] = content_value

                elif name_value == 'description':
                    item['description'] = content_value
                elif name_value == 'ColumnType':
                    item['category'] = content_value
                elif name_value == 'keywords':
                    item['keywords'] = content_value
                elif name_value == 'SiteDomain':
                    item['site_domain'] = content_value



        for tr in new_soup.find_all('tr'):
            try:
                td = tr.find('td', class_='bt_content')
                if td:
                    div = td.find('div', class_='art_con')
                    if div:
                        p_tags = div.find_all('p')
                        # texts = [p.get_text(strip=True) for p in p_tags]
                        texts = [p.get_text().replace(" ", "").replace("\n", "") for p in p_tags]
                        item['content'] = texts
            except Exception as e:
                print('Error:', e)  # 打印异常信息





        # 使用 yield 返回 Item 对象
        yield item

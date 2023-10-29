import scrapy
from bs4 import BeautifulSoup
from ..items import WendengItem
from scrapy_splash import SplashRequest

class WendengSearchSpider(scrapy.Spider):
    name = "wendeng_search"
    allowed_domains = ["www.wendeng.gov.cn"]

    def start_requests(self):
        for page_number in range(1700, 1800):
            print(page_number)
            url = f"http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={page_number}&pg=20&cateid=1122&tpl=1361&checkError=1"
            # yield scrapy.Request(url=f"http://www.wendeng.gov.cn/jsearchfront/search.do?websiteid=371081000500000&q=&p={page_number}&pg=20&cateid=1122&tpl=1361&checkError=1")
            yield SplashRequest(url, self.parse, args={'wait': 5})
    def parse(self, response):

        page_source=response.text

        soup = BeautifulSoup(page_source, 'lxml')
        div_tags = soup.find_all('div', class_='jcse-news-url')
        for div in div_tags:
            a_tags = div.find_all('a')
            for a in a_tags:
                link = a.string
                print("Link:", link)  # 添加这行打印语句
                if 'weihai' in link:
                    continue
                yield scrapy.Request(link, callback=self.parse_detail,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61'})

    def parse_detail(self, response):
        item = WendengItem()
        item['url'] = response.xpath("/html/head/meta[@name='url']/@content").extract_first()

        item['title'] = response.xpath("/html/head/meta[@name='ArticleTitle']/@content").extract_first()
        item['published'] = response.xpath("/html/head/meta[@name='PubDate']/@content").extract_first()
        item['description'] = response.xpath("/html/head/meta[@name='description']/@content").extract_first()
        item['category'] = response.xpath("/html/head/meta[@name='ColumnType']/@content").extract_first()
        item['keywords'] = response.xpath("/html/head/meta[@name='keywords']/@content").extract_first()
        item['site_domain'] = response.xpath("/html/head/meta[@name='SiteDomain']/@content").extract_first()
        # 使用 yield 返回 Item 对象
        item['content'] = response.xpath("//*[@id='zoom']").extract_first()
        # print(item)
        yield item

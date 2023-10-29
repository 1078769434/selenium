from scrapy import cmdline

# 用于运行 Scrapy 爬虫的命令，将 'your_spider_name' 替换为你的爬虫名称
cmdline.execute("scrapy crawl wendeng_search".split())

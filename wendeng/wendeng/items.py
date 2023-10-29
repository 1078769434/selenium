# import scrapy
#
# class WendengItem(scrapy.Item):
#     url = scrapy.Field()
#     title = scrapy.Field()
#     published = scrapy.Field()
#     description = scrapy.Field()
#     category = scrapy.Field()
#     keywords = scrapy.Field()
#     site_domain = scrapy.Field()
#     content = scrapy.Field()
import scrapy

class WendengItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    published = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    keywords = scrapy.Field()
    site_domain = scrapy.Field()
    content = scrapy.Field()

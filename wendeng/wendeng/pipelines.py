
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ARRAY, Boolean, func, update
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError


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

class SQLAlchemyPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('SQLALCHEMY_DB_SETTINGS')
        return cls(db_settings)

    def open_spider(self, spider):
        self.engine = create_engine(self.db_settings['database_url'])
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def process_item(self, item, spider):
        # 查询数据库，检查是否已存在相同的记录
        existing_record = self.session.query(WebPage).filter_by(url=item['url']).first()

        if existing_record is None:
            # 创建SQLAlchemy模型类的实例，并将抓取到的数据赋值给它
            web_page = WebPage()
            web_page.url = item['url']
            web_page.title = item['title']
            web_page.content = item['content']
            web_page.published = item['published']
            web_page.description = item['description']
            web_page.category = item['category']
            web_page.keywords = item['keywords']
            web_page.site_domain = item['site_domain']

            # 将模型实例添加到会话并提交
            self.session.add(web_page)
            try:
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
        else:

            update_statement = update(WebPage).values(content=item['content']).where(WebPage.url == item['url'])
            self.session.execute(update_statement)
            # 提交事务
            self.session.commit()
        return item
    def close_spider(self, spider):
        self.session.close()
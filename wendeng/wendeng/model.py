from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ARRAY, Boolean, func

from sqlalchemy.orm import declarative_base



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

from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    source = Column(String, index=True)
    published_at = Column(DateTime, index=True)
    content = Column(Text)
    countries = Column(String) # Comma separated list of GPE entities
    keywords = Column(String) # Comma separated top keywords
    cluster_id = Column(Integer, default=0) # For grouping similar stories

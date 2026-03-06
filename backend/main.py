from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .database import SessionLocal, engine, Base
from .models import Article

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fake News & Narrative Tracker API")

# Allow CORS for student 2 frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/news")
def get_news(
    skip: int = 0, 
    limit: int = 100, 
    country: Optional[str] = None, 
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    if country:
        query = query.filter(Article.countries.contains(country))
    if topic:
        query = query.filter(Article.keywords.contains(topic))
    
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return [{"id": a.id, "title": a.title, "url": a.url, "source": a.source, "published_at": a.published_at, "countries": a.countries, "keywords": a.keywords, "cluster_id": a.cluster_id} for a in articles]

@app.get("/api/trending")
def get_trending_topics(db: Session = Depends(get_db)):
    articles = db.query(Article.keywords).all()
    all_keywords = []
    for a in articles:
        if a[0]:
            all_keywords.extend([k.strip() for k in a[0].split(',') if k.strip()])
    
    from collections import Counter
    top_topics = Counter(all_keywords).most_common(10)
    return [{"topic": t[0], "count": t[1]} for t in top_topics]

@app.get("/api/regions")
def get_region_stats(db: Session = Depends(get_db)):
    articles = db.query(Article.countries).all()
    all_countries = []
    for a in articles:
        if a[0]:
            all_countries.extend([c.strip() for c in a[0].split(',') if c.strip()])
    
    from collections import Counter
    region_counts = Counter(all_countries).most_common(15)
    return [{"region": r[0], "count": r[1]} for r in region_counts]

@app.get("/api/timeline")
def get_timeline(topic: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(
        func.date(Article.published_at).label('date'),
        func.count(Article.id).label('count')
    )
    if topic:
        query = query.filter(Article.keywords.contains(topic))
    
    results = query.group_by('date').order_by('date').all()
    return [{"date": str(r[0]), "count": r[1]} for r in results]

@app.get("/api/clusters")
def get_clusters(db: Session = Depends(get_db)):
    query = db.query(
        Article.cluster_id, 
        func.count(Article.id).label('count'),
        func.min(Article.title).label('sample_title')
    ).group_by(Article.cluster_id).order_by(func.count(Article.id).desc()).limit(10)
    
    results = query.all()
    return [{"cluster_id": r[0], "article_count": r[1], "sample_title": r[2]} for r in results]

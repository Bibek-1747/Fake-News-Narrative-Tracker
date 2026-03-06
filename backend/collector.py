import feedparser
import spacy
from dateutil import parser
from rake_nltk import Rake
import nltk
from .database import SessionLocal, engine, Base
from .models import Article
from datetime import datetime

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# RSS feeds from different sources and regions
RSS_FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "NYT": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "Reuters": "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&hl=en-US&gl=US&ceid=US:en"
}

# Ensure nltk models are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    import subprocess
    subprocess.run(["python", "-m", "nltk.downloader", "stopwords", "punkt", "punkt_tab"])

# Load NLP models
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spacy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

rake = Rake()

def extract_countries(text):
    doc = nlp(text)
    countries = set()
    for ent in doc.ents:
        if ent.label_ == "GPE": # Geopolitical Entity
            countries.add(ent.text)
    return ",".join(list(countries))

def extract_keywords(text):
    rake.extract_keywords_from_text(text)
    # Get top 5 keywords
    return ",".join(rake.get_ranked_phrases()[:5])

def fetch_and_process():
    db = SessionLocal()
    for source, url in RSS_FEEDS.items():
        print(f"Fetching {source}...")
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Check if exists
            existing = db.query(Article).filter(Article.url == entry.link).first()
            if existing:
                continue
            
            title = entry.title
            content = entry.get('summary', title)
            try:
                published_at = parser.parse(entry.published).replace(tzinfo=None)
            except:
                published_at = datetime.utcnow()
            
            text_for_nlp = f"{title}. {content}"
            countries = extract_countries(text_for_nlp)
            keywords = extract_keywords(text_for_nlp)
            
            # Simple clustering: hash the top keyword
            top_keyword = keywords.split(',')[0] if keywords else "general"
            cluster_id = abs(hash(top_keyword)) % 1000

            article = Article(
                title=title,
                url=entry.link,
                source=source,
                published_at=published_at,
                content=content,
                countries=countries,
                keywords=keywords,
                cluster_id=cluster_id
            )
            db.add(article)
        db.commit()
    db.close()
    print("Data collection and processing complete.")

if __name__ == "__main__":
    fetch_and_process()

import pandas as pd
from database import SessionLocal
from models import Article

def export_processed_data():
    db = SessionLocal()
    # Query all articles
    articles = db.query(Article).all()
    
    if not articles:
        print("No data found in the database. Please run collector.py first.")
        db.close()
        return

    # Convert to a list of dictionaries
    data = []
    for a in articles:
        data.append({
            "id": a.id,
            "title": a.title,
            "url": a.url,
            "source": a.source,
            "published_at": a.published_at,
            "content_snippet": a.content[:200] + "..." if a.content else "",
            "extracted_countries": a.countries,
            "extracted_keywords": a.keywords,
            "topic_cluster_id": a.cluster_id
        })
    
    # Create DataFrame and export to CSV
    df = pd.DataFrame(data)
    output_filename = "processed_news_dataset.csv"
    df.to_csv(output_filename, index=False)
    
    print(f"Successfully generated processed dataset: {output_filename}")
    print(f"Total records exported: {len(data)}")
    
    db.close()

if __name__ == "__main__":
    export_processed_data()

# Fake News & Narrative Tracker 📰

## Problem Statement
The internet allows news and information to spread extremely quickly across websites, social media, and blogs. However, misinformation and misleading narratives can also spread rapidly and influence public opinion. This project tracks how news topics spread globally across different sources over time. The system collects news data, analyzes emerging topics, and visualizes how narratives evolve and spread across regions and timelines.

## Data Sources
This backend implementation collects news data from live, public RSS feeds belonging to global media organizations:
- **BBC Worldwide News**
- **Al Jazeera English**
- **The New York Times**
- **Reuters**

An automated collection script (`backend/collector.py`) fetches the latest news, processes it with Natural Language Processing (NLP) specifically for entity recognition and keyword extraction.

## Project Architecture
- **Backend**: Python with FastAPI
- **Database**: SQLite (managed with SQLAlchemy)
- **Data Collection**: `feedparser`
- **NLP & Processing**: `spaCy` (for Named Entity Recognition to detect Countries) & `rake-nltk` (for rapid automatic keyword extraction)

## Setup Instructions

### 1. Requirements
Ensure you have Python 3.9+ installed. Navigate to the project root directory and create a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Data Collection
Run the data collector to populate the database with fresh articles from global news sources. This script will automatically download the required NLP models if missing.
```bash
# Go back to the root directory
cd ..
python -m backend.collector
```

### 4. Run the API Server
Start the FastAPI development server:
```bash
uvicorn backend.main:app --reload
```

The server will start at `http://127.0.0.1:8000`. 
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### API Endpoints
- `GET /api/news` - Fetch recent news articles. Can filter by `?country=` or `?topic=`.
- `GET /api/trending` - Best topics and keywords extracted across the entire dataset.
- `GET /api/regions` - Top Geopolitical Regions mentioned.
- `GET /api/timeline` - A daily timeline of news coverage (can be filtered by topic).
- `GET /api/clusters` - Clusters of news stories reporting on similar events.

## Division of Work
This repository embodies the completion of **Student 1 – Data & Backend**, providing the robust API structure and real-world data foundation needed for **Student 2** to build the Web Application Visualization.

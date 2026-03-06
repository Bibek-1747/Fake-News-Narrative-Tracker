import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

def run_eda(csv_file="processed_news_dataset.csv"):
    if not os.path.exists(csv_file):
        print(f"Dataset {csv_file} not found. Please run export_data.py first.")
        return

    print("Loading dataset...")
    df = pd.DataFrame()
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
        
    if df.empty:
        print("Dataset is empty.")
        return

    print("--- Exploratory Data Analysis (EDA) ---")
    print(f"Total News Articles: {len(df)}")
    print("\n1. Data Overview:")
    print(df.info())
    
    print("\n2. Articles per Source:")
    source_counts = df['source'].value_counts()
    print(source_counts)

    # Visualization directory
    os.makedirs("eda_outputs", exist_ok=True)
    
    # Plot 1: Source Distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='source', order=df['source'].value_counts().index, palette='viridis')
    plt.title("Number of Articles per Source")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("eda_outputs/source_distribution.png")
    plt.close()
    
    # Plot 2: Keyword Wordcloud
    print("Generating WordCloud for Topics/Keywords...")
    all_keywords = df['extracted_keywords'].dropna().str.cat(sep=',')
    if all_keywords:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_keywords)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title("Trending Topics & Keywords")
        plt.tight_layout()
        plt.savefig("eda_outputs/topics_wordcloud.png")
        plt.close()

    # Plot 3: Top Countries/Regions
    print("\n3. Extracting Top Locations...")
    countries = df['extracted_countries'].dropna().str.split(',', expand=True).stack().str.strip()
    top_countries = countries.value_counts().head(10)
    print(top_countries)
    
    if not top_countries.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_countries.values, y=top_countries.index, palette='magma')
        plt.title("Top 10 Geopolitical Entities / Regions Mentioned")
        plt.xlabel("Number of Mentions")
        plt.ylabel("Region")
        plt.tight_layout()
        plt.savefig("eda_outputs/top_regions.png")
        plt.close()

    print("\nEDA completed successfully. Visualizations saved in 'eda_outputs' directory.")

if __name__ == "__main__":
    run_eda()

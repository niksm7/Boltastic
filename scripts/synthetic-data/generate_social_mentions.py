#!/usr/bin/env python3
"""
Generate synthetic social mentions data with sentiment anomalies.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_docs(count=700, days_back=14):
    """Generate synthetic social mentions documents."""
    platforms = ['Twitter', 'Facebook', 'LinkedIn', 'Instagram', 'Reddit']
    brands = ['Boltastic', 'TechCorp', 'CloudService', 'DataPlatform']
    authors = [f"user_{i}" for i in range(100, 500)]
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    # Normal baseline (sentiment ~0.3 to 0.7)
    positive_phrases = [
        "Great product!",
        "Love using this service",
        "Highly recommend",
        "Excellent customer support",
        "Best in class"
    ]
    negative_phrases = [
        "Not working properly",
        "Disappointed with service",
        "Poor experience",
        "Needs improvement",
        "Frustrating to use"
    ]
    neutral_phrases = [
        "Tried the new feature",
        "Interesting update",
        "Checking it out",
        "New release available"
    ]
    
    for i in range(int(count * 0.7)):
        timestamp = base_time + timedelta(
            hours=random.randint(0, days_back * 24),
            minutes=random.randint(0, 59)
        )
        
        sentiment_label = random.choice(['positive', 'negative', 'neutral'])
        if sentiment_label == 'positive':
            mention_text = random.choice(positive_phrases)
            sentiment_score = random.uniform(0.6, 0.9)
        elif sentiment_label == 'negative':
            mention_text = random.choice(negative_phrases)
            sentiment_score = random.uniform(0.1, 0.4)
        else:
            mention_text = random.choice(neutral_phrases)
            sentiment_score = random.uniform(0.4, 0.6)
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'platform': random.choice(platforms),
            'sentiment_score': round(sentiment_score, 3),
            'sentiment_label': sentiment_label,
            'mention_text': mention_text,
            'brand': random.choice(brands),
            'author_id': random.choice(authors),
            'author_name': f"@{random.choice(authors)}",
            'post_id': f"post_{random.randint(100000, 999999)}",
            'engagement.likes': random.randint(0, 500),
            'engagement.shares': random.randint(0, 100),
            'engagement.comments': random.randint(0, 50),
            'hashtags': random.sample(['tech', 'innovation', 'cloud', 'saas', 'startup'], k=random.randint(0, 3)),
            'language': 'en',
            'location': random.choice(['US', 'UK', 'CA', 'AU', None]),
        }
        docs.append({'_index': 'social-mentions-2025.02', '_source': doc})
    
    # Anomaly: Sentiment drop (last 2 days)
    anomaly_start = datetime.utcnow() - timedelta(days=2)
    for i in range(int(count * 0.3)):
        timestamp = anomaly_start + timedelta(
            hours=random.randint(0, 48),
            minutes=random.randint(0, 59)
        )
        
        mention_text = random.choice([
            "Service is down again!",
            "Very disappointed with recent changes",
            "Customer support is terrible",
            "Bugs everywhere",
            "Worst update ever"
        ])
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'platform': random.choice(['Twitter', 'Reddit']),
            'sentiment_score': round(random.uniform(0.05, 0.25), 3),  # Low sentiment
            'sentiment_label': 'negative',
            'mention_text': mention_text,
            'brand': 'Boltastic',
            'author_id': random.choice(authors),
            'author_name': f"@{random.choice(authors)}",
            'post_id': f"post_{random.randint(100000, 999999)}",
            'engagement.likes': random.randint(10, 200),
            'engagement.shares': random.randint(5, 50),
            'engagement.comments': random.randint(5, 30),
            'hashtags': ['complaint', 'bug', 'downtime'],
            'language': 'en',
            'location': random.choice(['US', 'UK']),
        }
        docs.append({'_index': 'social-mentions-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating social mentions data...")
    docs = generate_docs(count=700, days_back=14)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

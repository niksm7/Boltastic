#!/usr/bin/env python3
"""
Generate synthetic campaign metrics data with CTR anomalies.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_docs(count=600, days_back=14):
    """Generate synthetic campaign metrics documents."""
    campaigns = [f"campaign_{i:03d}" for i in range(1, 21)]
    channels = ['Google Ads', 'Facebook Ads', 'LinkedIn Ads', 'Twitter Ads', 'Display']
    audiences = ['B2B', 'B2C', 'Enterprise', 'SMB', 'Consumer']
    geographies = ['US', 'UK', 'CA', 'DE', 'FR', 'AU']
    devices = ['Desktop', 'Mobile', 'Tablet']
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    # Normal baseline (CTR ~2-4%)
    for i in range(int(count * 0.7)):
        timestamp = base_time + timedelta(
            hours=random.randint(0, days_back * 24),
            minutes=random.randint(0, 59)
        )
        
        impressions = random.randint(1000, 50000)
        clicks = int(impressions * random.uniform(0.02, 0.04))
        spend = impressions * random.uniform(0.5, 2.0)
        revenue = clicks * random.uniform(5, 25)
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'campaign_id': random.choice(campaigns),
            'campaign_name': f"Summer Sale {random.choice(campaigns)}",
            'ctr': clicks / impressions if impressions > 0 else 0,
            'impressions': impressions,
            'clicks': clicks,
            'spend': round(spend, 2),
            'revenue': round(revenue, 2),
            'conversions': int(clicks * random.uniform(0.05, 0.15)),
            'channel': random.choice(channels),
            'ad_group_id': f"adgroup_{random.randint(1, 50)}",
            'ad_id': f"ad_{random.randint(1, 200)}",
            'target_audience': random.choice(audiences),
            'geography': random.choice(geographies),
            'device_type': random.choice(devices),
        }
        docs.append({'_index': 'campaign-metrics-2025.02', '_source': doc})
    
    # Anomaly: CTR drop (last 3 days)
    anomaly_start = datetime.utcnow() - timedelta(days=3)
    for i in range(int(count * 0.3)):
        timestamp = anomaly_start + timedelta(
            hours=random.randint(0, 72),
            minutes=random.randint(0, 59)
        )
        
        impressions = random.randint(5000, 30000)
        clicks = int(impressions * random.uniform(0.005, 0.015))  # Low CTR
        spend = impressions * random.uniform(0.5, 2.0)
        revenue = clicks * random.uniform(5, 25)
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'campaign_id': 'campaign_015',  # Specific campaign with issue
            'campaign_name': 'Summer Sale campaign_015',
            'ctr': clicks / impressions if impressions > 0 else 0,
            'impressions': impressions,
            'clicks': clicks,
            'spend': round(spend, 2),
            'revenue': round(revenue, 2),
            'conversions': int(clicks * random.uniform(0.05, 0.15)),
            'channel': 'Google Ads',
            'ad_group_id': 'adgroup_25',
            'ad_id': 'ad_125',
            'target_audience': 'B2C',
            'geography': 'US',
            'device_type': random.choice(devices),
        }
        docs.append({'_index': 'campaign-metrics-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating campaign metrics data...")
    docs = generate_docs(count=600, days_back=14)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

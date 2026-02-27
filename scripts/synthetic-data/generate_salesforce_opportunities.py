#!/usr/bin/env python3
"""
Generate synthetic Salesforce opportunities data with stalled deals.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_docs(count=500, days_back=30):
    """Generate synthetic Salesforce opportunities documents."""
    stages = ['Prospecting', 'Qualification', 'Needs Analysis', 'Value Proposition', 'Id. Decision Makers', 'Perception Analysis', 'Proposal/Price Quote', 'Negotiation/Review', 'Closed Won', 'Closed Lost']
    owners = [f"sales_rep_{i:02d}" for i in range(1, 11)]
    accounts = [f"account_{i:03d}" for i in range(1, 51)]
    lead_sources = ['Website', 'Referral', 'Partner', 'Cold Call', 'Trade Show', 'Social Media']
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    # Normal opportunities
    for i in range(int(count * 0.7)):
        timestamp = base_time + timedelta(
            days=random.randint(0, days_back),
            hours=random.randint(0, 23)
        )
        
        last_activity = timestamp + timedelta(days=random.randint(0, 7))
        days_since_activity = (datetime.utcnow() - last_activity).days
        
        stage = random.choice(stages[:8])  # Exclude closed stages
        amount = random.uniform(10000, 500000)
        probability = random.uniform(0.2, 0.9)
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'opportunity_id': f"opp_{random.randint(10000, 99999)}",
            'opportunity_name': f"Deal with {random.choice(accounts)}",
            'stage': stage,
            'amount': round(amount, 2),
            'currency': 'USD',
            'close_date': (datetime.utcnow() + timedelta(days=random.randint(7, 90))).isoformat() + 'Z',
            'last_activity_at': last_activity.isoformat() + 'Z',
            'days_since_last_activity': days_since_activity,
            'owner_id': random.choice(owners),
            'owner_name': random.choice(owners).replace('_', ' ').title(),
            'account_id': random.choice(accounts),
            'account_name': random.choice(accounts).replace('_', ' ').title(),
            'probability': round(probability, 2),
            'lead_source': random.choice(lead_sources),
            'type': random.choice(['New Business', 'Existing Business', 'Renewal']),
            'is_closed': False,
            'is_won': False,
        }
        docs.append({'_index': 'salesforce-opportunities-2025.02', '_source': doc})
    
    # Anomaly: Stalled deals (no activity > 14 days)
    for i in range(int(count * 0.3)):
        timestamp = base_time + timedelta(
            days=random.randint(0, days_back - 14)
        )
        
        last_activity = timestamp  # Old activity
        days_since_activity = random.randint(15, 30)
        
        stage = random.choice(['Negotiation/Review', 'Proposal/Price Quote', 'Value Proposition'])
        amount = random.uniform(50000, 300000)
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'opportunity_id': f"opp_{random.randint(10000, 99999)}",
            'opportunity_name': f"Stalled Deal {random.choice(accounts)}",
            'stage': stage,
            'amount': round(amount, 2),
            'currency': 'USD',
            'close_date': (datetime.utcnow() + timedelta(days=random.randint(1, 30))).isoformat() + 'Z',
            'last_activity_at': last_activity.isoformat() + 'Z',
            'days_since_last_activity': days_since_activity,
            'owner_id': random.choice(owners),
            'owner_name': random.choice(owners).replace('_', ' ').title(),
            'account_id': random.choice(accounts),
            'account_name': random.choice(accounts).replace('_', ' ').title(),
            'probability': round(random.uniform(0.3, 0.7), 2),
            'lead_source': random.choice(lead_sources),
            'type': 'New Business',
            'is_closed': False,
            'is_won': False,
        }
        docs.append({'_index': 'salesforce-opportunities-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating Salesforce opportunities data...")
    docs = generate_docs(count=500, days_back=30)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Generate synthetic CRM activities data.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_docs(count=600, days_back=30):
    """Generate synthetic CRM activities documents."""
    activity_types = ['Call', 'Email', 'Meeting', 'Task', 'Note']
    outcomes = ['Completed', 'No Answer', 'Left Voicemail', 'Scheduled', 'Cancelled']
    accounts = [f"account_{i:03d}" for i in range(1, 51)]
    opportunities = [f"opp_{i}" for i in range(10000, 99999)]
    owners = [f"sales_rep_{i:02d}" for i in range(1, 11)]
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    for i in range(count):
        timestamp = base_time + timedelta(
            days=random.randint(0, days_back),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        activity_type = random.choice(activity_types)
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'activity_type': activity_type,
            'activity_subtype': random.choice(['Inbound', 'Outbound', 'Follow-up']) if activity_type == 'Call' else None,
            'account_id': random.choice(accounts),
            'account_name': random.choice(accounts).replace('_', ' ').title(),
            'opportunity_id': random.choice(opportunities) if random.random() > 0.3 else None,
            'opportunity_name': f"Deal {random.choice(opportunities)}" if random.random() > 0.3 else None,
            'outcome': random.choice(outcomes),
            'subject': f"{activity_type} with {random.choice(accounts)}",
            'description': f"Discussed {random.choice(['pricing', 'features', 'timeline', 'next steps'])}",
            'owner_id': random.choice(owners),
            'owner_name': random.choice(owners).replace('_', ' ').title(),
            'duration_minutes': random.randint(5, 60) if activity_type in ['Call', 'Meeting'] else None,
            'status': random.choice(['Completed', 'In Progress', 'Scheduled', 'Cancelled']),
            'priority': random.choice(['High', 'Medium', 'Low']),
            'related_to_type': random.choice(['Account', 'Opportunity', 'Contact']),
            'related_to_id': random.choice(accounts + opportunities),
        }
        docs.append({'_index': 'crm-activities-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating CRM activities data...")
    docs = generate_docs(count=600, days_back=30)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

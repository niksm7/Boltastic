#!/usr/bin/env python3
"""
Generate synthetic cost center data with cost anomalies.
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
    """Generate synthetic cost center documents."""
    cost_centers = ['Engineering', 'Marketing', 'Sales', 'Operations', 'Support', 'Infrastructure']
    services = ['Compute', 'Storage', 'Database', 'Network', 'CDN', 'Monitoring', 'API Gateway']
    service_types = ['AWS', 'GCP', 'Azure', 'Internal']
    regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
    departments = ['Product', 'Engineering', 'Marketing', 'Sales', 'Operations']
    projects = [f"project_{i:02d}" for i in range(1, 21)]
    incidents = [f"inc_{random.randint(1000, 9999)}" for _ in range(10)]
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    # Normal baseline
    for i in range(int(count * 0.7)):
        timestamp = base_time + timedelta(
            days=random.randint(0, days_back),
            hours=random.randint(0, 23)
        )
        
        usage_hours = random.uniform(1, 720)
        unit_cost = random.uniform(0.05, 2.0)
        cost = usage_hours * unit_cost
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'cost_center_id': random.choice(cost_centers).lower().replace(' ', '_'),
            'cost_center_name': random.choice(cost_centers),
            'cost': round(cost, 2),
            'currency': 'USD',
            'service': random.choice(services),
            'service_type': random.choice(service_types),
            'region': random.choice(regions),
            'incident_id': random.choice(incidents) if random.random() > 0.8 else None,
            'resource_type': random.choice(['EC2', 'S3', 'RDS', 'Lambda', 'CloudFront']),
            'resource_id': f"res_{random.randint(100000, 999999)}",
            'usage_hours': round(usage_hours, 2),
            'unit_cost': round(unit_cost, 2),
            'department': random.choice(departments),
            'project_id': random.choice(projects),
            'tags': random.sample(['production', 'staging', 'development', 'test'], k=random.randint(1, 2)),
        }
        docs.append({'_index': 'cost-centers-2025.02', '_source': doc})
    
    # Anomaly: Cost spike (last 3 days) - related to incident
    anomaly_start = datetime.utcnow() - timedelta(days=3)
    incident_id = 'inc_5001'  # Specific incident
    
    for i in range(int(count * 0.3)):
        timestamp = anomaly_start + timedelta(
            days=random.randint(0, 3),
            hours=random.randint(0, 23)
        )
        
        usage_hours = random.uniform(100, 1000)  # High usage
        unit_cost = random.uniform(1.0, 5.0)  # Higher cost
        cost = usage_hours * unit_cost
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'cost_center_id': 'infrastructure',
            'cost_center_name': 'Infrastructure',
            'cost': round(cost, 2),
            'currency': 'USD',
            'service': random.choice(['Compute', 'Database', 'Network']),
            'service_type': 'AWS',
            'region': 'us-east-1',
            'incident_id': incident_id,
            'resource_type': random.choice(['EC2', 'RDS', 'Lambda']),
            'resource_id': f"res_{random.randint(100000, 999999)}",
            'usage_hours': round(usage_hours, 2),
            'unit_cost': round(unit_cost, 2),
            'department': 'Operations',
            'project_id': 'project_01',
            'tags': ['production', 'incident'],
        }
        docs.append({'_index': 'cost-centers-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating cost centers data...")
    docs = generate_docs(count=600, days_back=30)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

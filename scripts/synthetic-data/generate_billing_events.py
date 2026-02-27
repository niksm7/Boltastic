#!/usr/bin/env python3
"""
Generate synthetic billing events data with revenue anomalies.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_docs(count=800, days_back=30):
    """Generate synthetic billing events documents."""
    event_types = ['invoice', 'payment', 'refund', 'subscription_start', 'subscription_end', 'upgrade', 'downgrade']
    customers = [f"customer_{i:04d}" for i in range(1, 201)]
    products = ['Basic Plan', 'Pro Plan', 'Enterprise Plan', 'Add-on Storage', 'Add-on API']
    payment_methods = ['Credit Card', 'Bank Transfer', 'PayPal', 'Stripe']
    regions = ['US', 'EU', 'APAC', 'LATAM']
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    # Normal baseline
    for i in range(int(count * 0.7)):
        timestamp = base_time + timedelta(
            days=random.randint(0, days_back),
            hours=random.randint(0, 23)
        )
        
        event_type = random.choice(event_types)
        amount = random.uniform(50, 5000) if event_type != 'refund' else random.uniform(-5000, -50)
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'event_type': event_type,
            'amount': round(amount, 2),
            'currency': 'USD',
            'customer_id': random.choice(customers),
            'customer_name': f"Customer {random.choice(customers)}",
            'product_id': random.choice(products).lower().replace(' ', '_'),
            'product_name': random.choice(products),
            'subscription_id': f"sub_{random.randint(10000, 99999)}" if 'subscription' in event_type else None,
            'invoice_id': f"inv_{random.randint(100000, 999999)}" if event_type in ['invoice', 'payment'] else None,
            'transaction_id': f"txn_{random.randint(1000000, 9999999)}" if event_type == 'payment' else None,
            'payment_method': random.choice(payment_methods) if event_type == 'payment' else None,
            'billing_period': f"{datetime.utcnow().strftime('%Y-%m')}" if event_type == 'invoice' else None,
            'region': random.choice(regions),
            'tax_amount': round(amount * 0.1, 2) if amount > 0 else 0,
            'discount_amount': round(amount * random.uniform(0, 0.2), 2) if random.random() > 0.7 else 0,
            'status': random.choice(['completed', 'pending', 'failed']),
        }
        docs.append({'_index': 'billing-events-2025.02', '_source': doc})
    
    # Anomaly: Revenue dip (last 5 days)
    anomaly_start = datetime.utcnow() - timedelta(days=5)
    for i in range(int(count * 0.3)):
        timestamp = anomaly_start + timedelta(
            days=random.randint(0, 5),
            hours=random.randint(0, 23)
        )
        
        # Lower amounts
        amount = random.uniform(20, 1000)  # Reduced revenue
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'event_type': random.choice(['payment', 'invoice']),
            'amount': round(amount, 2),
            'currency': 'USD',
            'customer_id': random.choice(customers),
            'customer_name': f"Customer {random.choice(customers)}",
            'product_id': 'basic_plan',
            'product_name': 'Basic Plan',
            'subscription_id': f"sub_{random.randint(10000, 99999)}",
            'invoice_id': f"inv_{random.randint(100000, 999999)}",
            'transaction_id': f"txn_{random.randint(1000000, 9999999)}",
            'payment_method': random.choice(payment_methods),
            'billing_period': f"{datetime.utcnow().strftime('%Y-%m')}",
            'region': random.choice(regions),
            'tax_amount': round(amount * 0.1, 2),
            'discount_amount': 0,
            'status': 'completed',
        }
        docs.append({'_index': 'billing-events-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating billing events data...")
    docs = generate_docs(count=800, days_back=30)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

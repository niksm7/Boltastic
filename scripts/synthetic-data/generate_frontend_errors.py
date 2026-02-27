#!/usr/bin/env python3
"""
Generate synthetic frontend error data with error spikes.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_docs(count=800, days_back=14):
    """Generate synthetic frontend error documents."""
    urls = [
        '/dashboard',
        '/products',
        '/checkout',
        '/profile',
        '/settings',
        '/api/users',
        '/api/orders'
    ]
    components = ['Header', 'ProductList', 'CheckoutForm', 'PaymentForm', 'UserProfile', 'SearchBar']
    browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
    error_types = ['TypeError', 'ReferenceError', 'SyntaxError', 'NetworkError', 'DOMException']
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    # Normal baseline
    for i in range(int(count * 0.6)):
        timestamp = base_time + timedelta(
            hours=random.randint(0, days_back * 24),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        error_type = random.choice(error_types)
        component = random.choice(components)
        
        url_path = random.choice(urls)
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'error': {
                'message': f"{error_type}: Cannot read property 'id' of undefined",
                'stack': f"Error: {error_type}\n    at {component}.render (component.js:45)\n    at ReactDOM.render (react-dom.js:123)",
                'type': error_type,
                'name': error_type,
            },
            'url': f"https://example.com{url_path}",
            'url_path': url_path,
            'user_agent': f"Mozilla/5.0 ({random.choice(browsers)})",
            'component': component,
            'component_name': component,
            'session_id': f"session_{random.randint(100000, 999999)}",
            'user_id': f"user_{random.randint(1000, 9999)}" if random.random() > 0.3 else None,
            'browser': {'name': random.choice(browsers), 'version': f"{random.randint(90, 120)}.0"},
            'os': {'name': random.choice(['Windows', 'macOS', 'Linux', 'iOS', 'Android'])},
            'viewport': {'width': random.choice([1920, 1366, 1440, 1536]), 'height': random.choice([1080, 768, 900, 864])},
        }
        docs.append({'_index': 'frontend-errors-2025.02', '_source': doc})
    
    # Anomaly: Error spike (last 4 hours)
    spike_start = datetime.utcnow() - timedelta(hours=4)
    for i in range(int(count * 0.4)):
        timestamp = spike_start + timedelta(
            hours=random.randint(0, 4),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        component = 'CheckoutForm'  # Focused component failure
        error_type = 'TypeError'
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'error': {
                'message': f"{error_type}: Cannot read property 'price' of null in {component}",
                'stack': f"Error: {error_type}\n    at {component}.calculateTotal (checkout.js:78)\n    at {component}.handleSubmit (checkout.js:123)",
                'type': error_type,
                'name': error_type,
            },
            'url': 'https://example.com/checkout',
            'url_path': '/checkout',
            'user_agent': 'Mozilla/5.0 (Chrome)',
            'component': component,
            'component_name': component,
            'session_id': f"session_{random.randint(100000, 999999)}",
            'user_id': f"user_{random.randint(1000, 9999)}",
            'browser': {'name': 'Chrome', 'version': '120.0'},
            'os': {'name': random.choice(['Windows', 'macOS'])},
            'viewport': {'width': 1920, 'height': 1080},
        }
        docs.append({'_index': 'frontend-errors-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating frontend errors data...")
    docs = generate_docs(count=800, days_back=14)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

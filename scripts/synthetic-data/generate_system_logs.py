#!/usr/bin/env python3
"""
Generate synthetic system logs data with anomalies for login failures.
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_docs(count=1000, days_back=14):
    """Generate synthetic system log documents."""
    hosts = ['web-server-01', 'web-server-02', 'api-server-01', 'api-server-02', 'db-server-01']
    users = ['alice', 'bob', 'charlie', 'diana', 'eve', 'frank', 'grace', 'henry']
    services = ['auth-service', 'api-gateway', 'user-service', 'payment-service', 'order-service']
    log_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG']
    actions = ['login', 'logout', 'api_call', 'database_query', 'cache_hit', 'cache_miss']
    
    base_time = datetime.utcnow() - timedelta(days=days_back)
    docs = []
    
    # Normal baseline
    for i in range(int(count * 0.7)):
        timestamp = base_time + timedelta(
            hours=random.randint(0, days_back * 24),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        action = random.choice(actions)
        outcome = 'success' if random.random() > 0.1 else 'failure'
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'log.level': random.choice(log_levels),
            'message': f"{action} {outcome} for user {random.choice(users)}",
            'host.name': random.choice(hosts),
            'host.ip': f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'event.action': action,
            'event.outcome': outcome,
            'user.name': random.choice(users),
            'user.id': f"user_{random.randint(1000, 9999)}",
            'service.name': random.choice(services),
            'service.version': f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
            'http.request.method': random.choice(['GET', 'POST', 'PUT', 'DELETE']) if action == 'api_call' else None,
            'http.response.status_code': random.choice([200, 201, 400, 404, 500]) if action == 'api_call' else None,
        }
        
        if outcome == 'failure':
            doc['error.type'] = random.choice(['AuthenticationError', 'AuthorizationError', 'ValidationError'])
            doc['error.message'] = f"Failed to {action}: {random.choice(['Invalid credentials', 'Session expired', 'Permission denied'])}"
        
        docs.append({'_index': 'system-logs-2025.02', '_source': doc})
    
    # Anomaly: Login failure spike (last 2 days)
    anomaly_start = datetime.utcnow() - timedelta(days=2)
    for i in range(int(count * 0.2)):
        timestamp = anomaly_start + timedelta(
            hours=random.randint(0, 48),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'log.level': 'ERROR',
            'message': f"login failure for user {random.choice(users)}",
            'host.name': random.choice(hosts),
            'host.ip': f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'event.action': 'login',
            'event.outcome': 'failure',
            'user.name': random.choice(users),
            'user.id': f"user_{random.randint(1000, 9999)}",
            'service.name': 'auth-service',
            'error.type': 'AuthenticationError',
            'error.message': 'Invalid credentials',
            'http.response.status_code': 401,
        }
        docs.append({'_index': 'system-logs-2025.02', '_source': doc})
    
    # Anomaly: Error spike (last 6 hours)
    error_spike_start = datetime.utcnow() - timedelta(hours=6)
    for i in range(int(count * 0.1)):
        timestamp = error_spike_start + timedelta(
            hours=random.randint(0, 6),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        doc = {
            '@timestamp': timestamp.isoformat() + 'Z',
            'log.level': 'ERROR',
            'message': f"Database connection timeout in {random.choice(services)}",
            'host.name': random.choice(hosts),
            'host.ip': f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'event.action': 'database_query',
            'event.outcome': 'failure',
            'service.name': random.choice(services),
            'error.type': 'DatabaseError',
            'error.message': 'Connection timeout after 30s',
            'http.response.status_code': 503,
        }
        docs.append({'_index': 'system-logs-2025.02', '_source': doc})
    
    return docs

def main():
    """Main execution."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    client = Elasticsearch([es_url], api_key=api_key, request_timeout=60)
    
    print("Generating system logs data...")
    docs = generate_docs(count=1000, days_back=14)
    
    print(f"Indexing {len(docs)} documents...")
    success, failed = bulk(client, docs, chunk_size=500, request_timeout=60)
    
    print(f"✓ Successfully indexed {success} documents")
    if failed:
        print(f"✗ Failed to index {len(failed)} documents")

if __name__ == '__main__':
    main()

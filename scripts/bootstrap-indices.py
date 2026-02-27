#!/usr/bin/env python3
"""
Bootstrap script to create index templates and indices in Elastic Serverless.
"""

import os
import json
import sys
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
from dotenv import load_dotenv

load_dotenv()

def load_env():
    """Load environment variables."""
    es_url = os.getenv('ELASTICSEARCH_URL')
    api_key = os.getenv('ELASTIC_API_KEY')
    
    if not es_url or not api_key:
        print("Error: ELASTICSEARCH_URL and ELASTIC_API_KEY must be set")
        sys.exit(1)
    
    return es_url, api_key

def create_client(es_url, api_key):
    """Create Elasticsearch client."""
    return Elasticsearch(
        [es_url],
        api_key=api_key,
        request_timeout=30
    )

def deploy_index_template(client, template_path):
    """Deploy an index template."""
    template_name = template_path.stem
    
    with open(template_path, 'r') as f:
        template_body = json.load(f)
    
    try:
        client.indices.put_index_template(
            name=f"boltastic-{template_name}",
            body=template_body
        )
        print(f"✓ Deployed index template: boltastic-{template_name}")
        return True
    except RequestError as e:
        if e.error == 'resource_already_exists_exception':
            print(f"⚠ Index template already exists: boltastic-{template_name}")
            return True
        print(f"✗ Failed to deploy template {template_name}: {e}")
        return False

def main():
    """Main execution."""
    es_url, api_key = load_env()
    client = create_client(es_url, api_key)
    
    templates_dir = Path(__file__).parent.parent / 'elastic' / 'index-templates'
    
    if not templates_dir.exists():
        print(f"Error: Templates directory not found: {templates_dir}")
        sys.exit(1)
    
    template_files = list(templates_dir.glob('*.json'))
    
    if not template_files:
        print("No template files found")
        sys.exit(1)
    
    print(f"Deploying {len(template_files)} index templates...\n")
    
    success_count = 0
    for template_file in sorted(template_files):
        if deploy_index_template(client, template_file):
            success_count += 1
    
    print(f"\n✓ Successfully deployed {success_count}/{len(template_files)} templates")
    
    # Test connection
    try:
        info = client.info()
        print(f"\n✓ Connected to Elasticsearch cluster: {info['cluster_name']}")
    except Exception as e:
        print(f"\n✗ Failed to verify connection: {e}")

if __name__ == '__main__':
    main()

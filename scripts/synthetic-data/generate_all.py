#!/usr/bin/env python3
"""
Generate all synthetic data for Boltastic platform.
"""

import sys
from pathlib import Path

# Import all generators
from generate_system_logs import main as gen_system_logs
from generate_frontend_errors import main as gen_frontend_errors
from generate_campaign_metrics import main as gen_campaign_metrics
from generate_social_mentions import main as gen_social_mentions
from generate_salesforce_opportunities import main as gen_salesforce_opps
from generate_crm_activities import main as gen_crm_activities
from generate_billing_events import main as gen_billing_events
from generate_cost_centers import main as gen_cost_centers
from dotenv import load_dotenv

load_dotenv()

def main():
    """Generate all synthetic data."""
    generators = [
        ("System Logs", gen_system_logs),
        ("Frontend Errors", gen_frontend_errors),
        ("Campaign Metrics", gen_campaign_metrics),
        ("Social Mentions", gen_social_mentions),
        ("Salesforce Opportunities", gen_salesforce_opps),
        ("CRM Activities", gen_crm_activities),
        ("Billing Events", gen_billing_events),
        ("Cost Centers", gen_cost_centers),
    ]
    
    print("=" * 60)
    print("Boltastic Synthetic Data Generation")
    print("=" * 60)
    print()
    
    for name, generator in generators:
        print(f"\n[{name}]")
        print("-" * 60)
        try:
            generator()
        except Exception as e:
            print(f"✗ Error generating {name}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("✓ Data generation complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()

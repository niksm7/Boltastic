import csv

# Define the sample data for the Deal Intervention custom object
intervention_data = [
    {
        "Name": "Save GlobalCorp Deal",
        "Related_Opportunity_ID__c": "0068c00000abcdEAAQ",
        "Risk_Factor__c": "Stalled > 14 Days",
        "Agent_Reasoning__c": "No email or meeting activity detected in the last 15 days. Opportunity is stuck in the Negotiation stage. Recommended action: Trigger Play-001 (Value ROI case study).",
        "Status__c": "New"
    },
    {
        "Name": "TechNova Competitor Threat",
        "Related_Opportunity_ID__c": "0068c00000abcdFAAQ",
        "Risk_Factor__c": "Competitor Mention: TechNova",
        "Agent_Reasoning__c": "Prospect explicitly mentioned TechNova's pricing in the latest call transcript. High-value deal ($150k). Needs immediate Sales Engineering support per Play-002.",
        "Status__c": "In Progress"
    },
    {
        "Name": "Acme Corp - Lost Champion",
        "Related_Opportunity_ID__c": "0068c00000abcdGAAQ",
        "Risk_Factor__c": "Loss of Champion",
        "Agent_Reasoning__c": "Primary contact Sarah Jenkins has left the company based on recent email bounce-backs. Deal momentum has stopped entirely. Need to map out remaining buying committee.",
        "Status__c": "New"
    },
    {
        "Name": "Initech Pricing Pushback",
        "Related_Opportunity_ID__c": "0068c00000abcdHAAQ",
        "Risk_Factor__c": "Pricing Objection",
        "Agent_Reasoning__c": "Client is requesting a 30% discount, which exceeds standard rep limits. Deal velocity has slowed dramatically. Executive intervention required to pivot to Total Cost of Ownership.",
        "Status__c": "New"
    }
]

filename = "deal_interventions_upload.csv"

# Create the CSV file
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    # Match the field names exactly to your Salesforce API names
    fieldnames = ["Name", "Related_Opportunity_ID__c", "Risk_Factor__c", "Agent_Reasoning__c", "Status__c"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(intervention_data)

print(f"Successfully generated {filename}. Ready for Salesforce import.")
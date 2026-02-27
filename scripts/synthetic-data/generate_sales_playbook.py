import csv

# Define the data for the Sales Playbook custom object
playbook_data = [
    {
        "Name": "Play-001",
        "Trigger_Condition__c": "Stalled > 14 Days",
        "Action_Plan__c": "Send the 'Value ROI' case study. If no response in 48 hours, escalate to the Regional Director to initiate a multi-threading email to the prospect's VP.",
        "Required_Approval__c": "None"
    },
    {
        "Name": "Play-002",
        "Trigger_Condition__c": "Competitor Mention: TechNova",
        "Action_Plan__c": "Deploy the 'TechNova Takedown' deck. Emphasize our superior API uptime and dedicated CSM support. Offer a free 2-week technical PoC.",
        "Required_Approval__c": "Sales Engineering Manager"
    },
    {
        "Name": "Play-003",
        "Trigger_Condition__c": "Pricing Objection",
        "Action_Plan__c": "Pivot the conversation to Total Cost of Ownership (TCO). Do not immediately discount. If pushed, offer a maximum 10% discount on onboarding fees only.",
        "Required_Approval__c": "VP of Sales"
    },
    {
        "Name": "Play-004",
        "Trigger_Condition__c": "Loss of Champion",
        "Action_Plan__c": "Immediately pause technical discussions. Map out the remaining buying committee on LinkedIn. Request an intro to the new decision-maker from the departing champion.",
        "Required_Approval__c": "None"
    }
]

filename = "sales_playbooks_upload.csv"

# Create the CSV file
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Trigger_Condition__c", "Action_Plan__c", "Required_Approval__c"])
    writer.writeheader()
    writer.writerows(playbook_data)

print(f"Successfully generated {filename}. You can now import this into Salesforce.")
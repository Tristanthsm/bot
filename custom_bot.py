import json

# Load the workflow definition from workflow.json
with open('workflow.json', 'r', encoding='utf-8') as f:
    workflow = json.load(f)

# Print the workflow name
print(f"Workflow name: {workflow.get('name', 'unknown')}")

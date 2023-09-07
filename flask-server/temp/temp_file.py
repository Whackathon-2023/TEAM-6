import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
jira_data = pd.read_csv('JIRA_ITSD_FY23_FULL.csv')

# Filter the data to only consider 'Resolved' tickets
resolved_tickets = jira_data[jira_data['Status'] == 'Resolved']

# Count the number of tickets for each category
ticket_counts = resolved_tickets['Issue_Type'].value_counts()

# Create the log-linear graph
plt.figure(figsize=(10,6))
plt.bar(ticket_counts.index, ticket_counts.values)
plt.yscale('log')
plt.xlabel('Issue Types')
plt.ylabel('Counts')
plt.title('Log-Linear Plot of Issue Types vs Counts')
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig('issue_type_distribution.png')
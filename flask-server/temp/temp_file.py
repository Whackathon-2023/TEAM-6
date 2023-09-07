import matplotlib.pyplot as plt

# Data
names = ['Adam Ward', 'Devin Roberts', 'Diana Jimenez', 'Erin Porter', 'Heidi Vance', 'James Sheppard', 'Joel Johnson', 'John Brown', 'John Rich', 'Kimberly House', 'Matthew Hutchinson', 'Michael Williams', 'Shannon Newman', 'Sonya Luna', 'Stephen Haney']
tickets_resolved = [1743, 1713, 1729, 1743, 1818, 1817, 1802, 1735, 1764, 1782, 1770, 1732, 1743, 1810, 1763]

# Creating bar chart
plt.bar(names, tickets_resolved, color = 'blue')
plt.xlabel('Names')
plt.ylabel('Tickets Resolved')
plt.title('Number of Tickets Resolved by Each Person')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure
plt.savefig('tickets_resolved.png')
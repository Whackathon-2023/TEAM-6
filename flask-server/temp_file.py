import matplotlib.pyplot as plt

# Initialize data
name_ticket_data =[('Adam Ward', 1743), ('Devin Roberts', 1713), ('Diana Jimenez', 1729), ('Erin Porter', 1743), ('Heidi Vance', 1818), ('James Sheppard', 1817), ('Joel Johnson', 1802), ('John Brown', 1735), ('John Rich', 1764), ('Kimberly House', 1782), ('Matthew Hutchinson', 1770), ('Michael Williams', 1732), ('Shannon Newman', 1743), ('Sonya Luna', 1810), ('Stephen Haney', 1763)]

# Separate names and tickets resolved
names = [x[0] for x in name_ticket_data]
tickets_resolved = [x[1] for x in name_ticket_data]

# Creating the bar plot
plt.bar(names, tickets_resolved)
plt.xlabel('Names')
plt.xticks(rotation=90)
plt.ylabel('Tickets resolved')
plt.title('Number of tickets resolved by each person')

# Saving the plot
plt.tight_layout()
plt.savefig('tickets_resolved_per_person.png')
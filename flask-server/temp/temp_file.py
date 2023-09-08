import matplotlib.pyplot as plt

# Define the data
data = [(None, 21135), ('User Access', 2321), ('Business System', 2294), ('Computer', 606), ('Client Application', 517)]

# Unpack the data
labels, values = zip(*data)

# Create the bar chart
plt.bar(labels, values)

# Add a title and labels to the axes
plt.title('5 Most Common Problems for Service Desk Employees')
plt.xlabel('Problem Category')
plt.ylabel('Frequency')

# Save the figure
plt.savefig('common_problems.png')
plt.close()
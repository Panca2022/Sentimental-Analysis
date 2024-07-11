import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = r"F:\Projects\Intel\Review_Analysis\sentiment_analysis_12gen_DesktopProcessor.xlsx"
df = pd.read_excel(file_path)

# Print the column names to verify their existence
print("Columns in the DataFrame:", df.columns)

# Calculate the total count for each sentiment category
# Replace 'Sentiment Category' with the actual column name from your DataFrame
sentiment_counts = df['Sentiment Category'].value_counts()

# Create a pie chart
labels = sentiment_counts.index
sizes = sentiment_counts.values
colors = ['red', 'orange', 'gray', 'lightblue', 'green']

# Define explode values - ensure it matches the length of sizes and labels
explode = [0.1 if i == 0 else 0 for i in range(len(sizes))]  # Explode the first slice ('Very Negative')

plt.figure(figsize=(10, 8))  # Adjusted figure size
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Sentiment Distribution of Reviews')
plt.axis('equal')

# Add legend with adjusted placement
plt.legend(loc="best", bbox_to_anchor=(0.5, 0.5, 0.5, 0.5), fontsize='medium')

# Save the pie chart as a PNG file
plt.savefig(r"F:\Projects\Intel\Review_Analysis\sentiment_distribution.png", bbox_inches='tight')

# Show the pie chart
plt.show()

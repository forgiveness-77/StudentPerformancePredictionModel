import pandas as pd

# Create DataFrame
df = pd.read_csv('StudentPerformance.csv')

# Categorization function
def categorize_student(study_hours, sleep_hours):
    if 7 <= sleep_hours <= 8 and 4 <= study_hours <= 6:
        return "Optimal Balance"
    elif sleep_hours < 6 and study_hours > 6:
        return "Stressed Burnout"
    elif sleep_hours > 9 and study_hours < 3:
        return "Underengaged"
    elif 6 <= sleep_hours <= 7 and study_hours > 8:
        return "Inefficient High Effort"
    elif sleep_hours > 9 and study_hours >= 3:
        return "Recovery Needed"
    else:
        return "Moderate"

# Add category column
df['Category'] = df.apply(lambda row: categorize_student(row['Hours Studied'], row['Sleep Hours']), axis=1)

# Show summary
print("\nCategory Summary:")
print("=" * 50)
for category in df['Category'].unique():
    count = (df['Category'] == category).sum()
    print(f"{category}: {count} students")

# Save to CSV
df.to_csv('categorized_students.csv', index=False)
print("\n✅ Data saved to 'categorized_students.csv'")
# import pandas as pd
# from performance.models import StudentPerformance
# def run():
#     df = pd.read_csv('StudentPerformance.csv')
#     for _, row in df.iterrows():
#         StudentPerformance.objects.create(
#             hours_studied=row['Hours Studied'],
#             previous_scores=row['Previous Scores'],
#             extracurricular=row['Extracurricular Activities'] == 'Yes',
#             sleep_hours=row['Sleep Hours'],
#             sample_papers=row['Sample Question Papers Practiced'],
#             performance_index=row['Performance Index'],
#     )

import pandas as pd
from performance.models import StudentPerformance

def run():
    df = pd.read_csv('categorized_students.csv')
    
    # Clear existing data (optional)
    # StudentPerformance.objects.all().delete()
    
    students = []
    for _, row in df.iterrows():
        # Direct mapping from CSV columns to model fields
        student = StudentPerformance(
            hours_studied=row['Hours Studied'],
            previous_scores=row['Previous Scores'],
            extracurricular=row['Extracurricular Activities'] == 'Yes',
            sleep_hours=row['Sleep Hours'],
            sample_papers=row['Sample Question Papers Practiced'],
            performance_index=row['Performance Index'],
            category=row['Category']  # Direct from CSV!
        )
        students.append(student)
    
    # Bulk create for efficiency
    StudentPerformance.objects.bulk_create(students)
    print(f"✅ Loaded {len(students)} students with categories")
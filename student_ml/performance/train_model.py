import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# def train():
#     df = pd.read_csv('StudentPerformance.csv')
#     df['Extracurricular Activities'] = LabelEncoder().fit_transform(
#     df['Extracurricular Activities']
#     )
#     X = df.drop('Performance Index', axis=1)
#     y = df['Performance Index']
#     X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
#     )
#     model = RandomForestRegressor(n_estimators=200, random_state=42)
#     model.fit(X_train, y_train)
#     joblib.dump(model, 'performance/model.pkl')
#     print("Model trained and saved")
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

def train():
    df = pd.read_csv('categorized_students.csv')
    
    # Encode only Extracurricular Activities
    le_extra = LabelEncoder()
    df['Extracurricular Activities'] = le_extra.fit_transform(df['Extracurricular Activities'])
    
    # Train on ALL data (including bad categories)
    X = df.drop(['Performance Index', 'Category'], axis=1)  # Remove Category from training
    y = df['Performance Index']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    
    # Save
    joblib.dump(model, 'performance/model.pkl')
    joblib.dump(le_extra, 'performance/le_extra.pkl')
    
    print(f"Model trained on {len(df)} samples")
    print(f"R² score: {model.score(X_test, y_test):.4f}")
    print("✅ Single model saved - use category check during prediction")

train()
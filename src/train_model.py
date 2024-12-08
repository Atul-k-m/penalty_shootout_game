import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('../data/advanced_shots_data.csv')

features = ['shot_x', 'shot_y', 'shot_power', 'shot_angle', 
            'goalkeeper_skill', 'goalkeeper_reaction_time']
X = data[features]
y = data['goal_scored']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


models = {
    'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=200, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    results[name] = {
        'model': model,
        'classification_report': classification_report(y_test, y_pred),
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    }
    
   
    print(f"\n{name} Results:")
    print(results[name]['classification_report'])


plt.figure(figsize=(10, 6))
feature_importances = results['Random Forest']['model'].feature_importances_
sns.barplot(x=feature_importances, y=features)
plt.title('Feature Importances in Goal Prediction')
plt.xlabel('Importance')
plt.tight_layout()
plt.savefig('../models/feature_importances.png')


best_model = results['Random Forest']['model']
joblib.dump({
    'model': best_model, 
    'scaler': scaler
}, '../models/advanced_goalkeeper_model.pkl')

print("Advanced model saved successfully!")
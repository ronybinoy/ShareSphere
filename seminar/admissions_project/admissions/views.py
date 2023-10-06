from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from .models import AdmissionPrediction
from sklearn.model_selection import train_test_split

# Load the saved model
stack = joblib.load('stacking_classifier.pkl')

def home(request):
    return render(request, 'home.html')

def predict_admission(request):
    if request.method == 'POST':
        percentage_12th = float(request.POST['percentage_12th'])
        GRE_Score = float(request.POST['GRE_Score'])
        TOEFL_Score = float(request.POST['TOEFL_Score'])
        CGPA = float(request.POST['CGPA'])

        # Load your original dataset or perform preprocessing as needed
        df = pd.read_csv('updated_data.csv')

        # Assuming 'Chance of Admit' is your target variable
        threshold = 0.5
        y = (df['Chance of Admit'] > threshold).astype(int)
        X = df.drop(['Serial No.', 'Chance of Admit'], axis=1)

        # Split the data into training and testing sets (80% training, 20% testing)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Save the testing data
        testing_data = pd.concat([X_test, y_test], axis=1)
        testing_data.to_csv('testing_data.csv', index=False)

        input_data = pd.DataFrame({
            '12th Percentage': [percentage_12th],
            'GRE Score': [GRE_Score],
            'TOEFL Score': [TOEFL_Score],
            'CGPA': [CGPA],
        })

        probability = stack.predict_proba(input_data)[:, 1]

        # Make predictions on the testing data
        y_pred_probabilities = stack.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_probabilities > threshold).astype(int)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        # Write the inputs and results to the AdmissionPrediction table
        admission_prediction = AdmissionPrediction.objects.create(
            percentage_12th=percentage_12th,
            GRE_Score=GRE_Score,
            TOEFL_Score=TOEFL_Score,
            CGPA=CGPA,
            probability=probability[0],
            accuracy=accuracy,
            precision=precision,
            recall=recall
        )

        # Save the entry to the database
        admission_prediction.save()

        return render(request, 'home.html', {
            'probability': probability[0],
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
        })

    return HttpResponse("Invalid Request")

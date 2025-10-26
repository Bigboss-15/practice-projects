import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def create_model():
    # Expanded dataset for better training/testing
    data = {
        'hours_studied': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'Score': [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98, 100]
    }

    df = pd.DataFrame(data)
    df['pass'] = (df['Score'] >= 50).astype(int)
    
    X = df[['hours_studied']]
    y = df['pass']
    
    # Using a larger test size for better evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Using LogisticRegression for classification task
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, accuracy

def predict_pass_fail(model, hours):
    prediction = model.predict([[hours]])
    probability = model.predict_proba([[hours]])
    
    result = "PASS" if prediction[0] == 1 else "FAIL"
    confidence = max(probability[0]) * 100
    
    return result, confidence

def main():
    print("=== Student Performance Predictor ===")
    print("This application predicts if a student will pass based on study hours.")
    print()
    
    # Create and train the model
    print("Training model...")
    model, accuracy = create_model()
    print(f"Model trained with {accuracy*100:.1f}% accuracy on test set.")
    print()
    
    # Application loop
    while True:
        try:
            print("Enter study hours (or 'quit' to exit):")
            user_input = input("> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the Student Performance Predictor!")
                break
            
            hours = float(user_input)
            
            if hours < 0:
                print("Please enter a positive number of hours.")
                continue
                
            result, confidence = predict_pass_fail(model, hours)
            
            print(f"\nPrediction: {result}")
            print(f"Confidence: {confidence:.1f}%")
            
            if result == "PASS":
                print("Great job! Based on your study hours, you're likely to pass!")
            else:
                print("You might want to study more to increase your chances of passing.")
            
            print("-" * 40)
            print()
            
        except ValueError:
            print("Please enter a valid number or 'quit' to exit.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
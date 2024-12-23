from flask import Flask, render_template, redirect, request, url_for
import joblib

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        try:
            # Get user inputs
            amount = float(request.form["amount"])
            oldbalanceOrg = float(request.form["oldbalanceOrg"])
            newbalanceOrig = float(request.form["newbalanceOrig"])

            # Prepare data for prediction
            new_values = [[amount, oldbalanceOrg, newbalanceOrig]]
            
            # Load the AdaBoost model
            model = joblib.load("models/adaboost_model.pkl")
            
            # Make prediction
            pred = model.predict(new_values)
            
            # Map prediction to a user-friendly message
            result = "Fraudulent" if pred[0] == 1 else "Non-Fraudulent"

            return render_template("prediction.html", result=result)
        except Exception as e:
            return render_template("prediction.html", error=str(e))

    # Render the input form template
    return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True)

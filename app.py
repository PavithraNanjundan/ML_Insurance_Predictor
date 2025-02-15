from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import statsmodels.api as sm
import pickle

app = Flask(__name__)

# Load the trained model (Assuming model is saved as 'model.pkl')
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = request.form.get("age", type=int)
        bmi = request.form.get("bmi", type=float)
        children = request.form.get("children", type=int)
        smoker_yes = request.form.get("smoker_yes", type=int)
        
        df = pd.DataFrame([[age, bmi, children, smoker_yes]], columns=['age', 'bmi', 'children', 'smoker_yes'])

        
        # Make prediction
        prediction = model.predict(df)
        
        return render_template("index.html", result=round(float(prediction[0][0]), 2), original_input=request.form)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

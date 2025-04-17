
from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form and print for debug
        engine_size = request.form['engine_size']
        cylinders = request.form['cylinders']
        transmission = request.form['transmission']
        fuel_type = request.form['fuel_type']

        print("Received input:", engine_size, cylinders, transmission, fuel_type)

        # Construct DataFrame
        input_df = pd.DataFrame([{
            'engine_size': float(engine_size),
            'cylinders': int(cylinders),
            'transmission': transmission,
            'fuel_type': fuel_type
        }])

        # Predict
        prediction = model.predict(input_df)
        result = f"Predicted Fuel Efficiency: {prediction[0]:.2f} MPG"
        return render_template('index.html', prediction_text=result)

    except Exception as e:
        print("Prediction error:", e)
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(debug=True)

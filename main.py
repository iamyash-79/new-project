from flask import Flask, render_template, request, jsonify
import sqlite3, joblib
import pandas as pd

app = Flask(__name__)

# ✅ Load ML model properly
model = joblib.load('model.pkl')

# Helper for potential future use
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('slide.html', prediction_text=None)

@app.route('/slide')
def next_page():
    return render_template('slide.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def index():
    return render_template('index.html', prediction_text=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        engine_size = float(request.form['engine_size'])
        cylinders = int(request.form['cylinders'])
        transmission = request.form['transmission']
        fuel_type = request.form['fuel_type']

        input_df = pd.DataFrame([{
            'Engine_Size(L)': engine_size,
            'Cylinders': cylinders,
            'Transmission': transmission,
            'Fuel Type': fuel_type
        }])  # 👈 Column names match training CSV exactly

        prediction = model.predict(input_df)
        mpg = prediction[0]
        kmpl = mpg * 0.425144  # Convert to KMPL

        result = f"🚗 Predicted Fuel Efficiency: {mpg:.2f} MPG ({kmpl:.2f} KMPL)"
        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return render_template('index.html', prediction_text=f"🚫 Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

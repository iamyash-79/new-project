from flask import Flask, render_template, request, redirect, session, url_for
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy user credentials (email:password)
USERS = {
    "user@example.com": "password123"
}

# Load model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html', session=session, prediction_text=None)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if USERS.get(email) == password:
        session['logged_in'] = True
        session['email'] = email
        return redirect(url_for('home'))
    else:
        return render_template('index.html', prediction_text="Invalid login. Try again.", session=session)

@app.route('/predict', methods=['POST'])
def predict():
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    try:
        engine_size = float(request.form['engine_size'])
        cylinders = int(request.form['cylinders'])
        transmission = request.form['transmission']
        fuel_type = request.form['fuel_type']

        input_df = pd.DataFrame([{
            'engine_size': engine_size,
            'cylinders': cylinders,
            'transmission': transmission,
            'fuel_type': fuel_type
        }])

        prediction = model.predict(input_df)
        result = f"Predicted Fuel Efficiency: {prediction[0]:.2f} MPG"

        return render_template('index.html', prediction_text=result, session=session)
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}", session=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


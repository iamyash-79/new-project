from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load ML model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Helper to connect to database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html', session=session, prediction_text=None)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
    conn.close()

    if user:
        session['logged_in'] = True
        session['email'] = user['email']
        return redirect(url_for('home'))
    else:
        return render_template('index.html', prediction_text="Invalid login. Try again.", session=session)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', message="Passwords do not match.")
        if not name or not mobile or not email or not password:
            return render_template('register.html', message="Please fill in all required fields.")

        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            conn.close()
            return render_template('register.html', message="Email already exists.")

        conn.execute('INSERT INTO users (name, mobile, email, password) VALUES (?, ?, ?, ?)',
                     (name, mobile, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('register.html', message=None)

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

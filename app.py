from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Load your trained model
model = joblib.load('model.pkl')

# Welcome page route
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Sign-in page route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Replace this with actual authentication logic
        if username == 'admin' and password == '060':  # Simple example
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('signin.html', error='Invalid credentials')
    
    return render_template('signin.html')

# Home page route (Network Intrusion Detection System form)
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('index.html')

# Sign-out route
@app.route('/signout')
def signout():
    session.pop('user', None)  # Remove user session
    return redirect(url_for('welcome'))


# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('signin'))
    
    int_features = [float(x) for x in request.form.values()]
    
    # Feature processing logic here
    if int_features[0] == 0:
        f_features = [0, 0, 0] + int_features[1:]
    elif int_features[0] == 1:
        f_features = [1, 0, 0] + int_features[1:]
    elif int_features[0] == 2:
        f_features = [0, 1, 0] + int_features[1:]
    else:
        f_features = [0, 0, 1] + int_features[1:]

    if f_features[6] == 0:
        fn_features = f_features[:6] + [0, 0] + f_features[7:]
    elif f_features[6] == 1:
        fn_features = f_features[:6] + [1, 0] + f_features[7:]
    else:
        fn_features = f_features[:6] + [0, 1] + f_features[7:]

    final_features = [np.array(fn_features)]
    prediction = model.predict(final_features)
    
    # Determine output based on prediction
    output = 'Unknown'
    if prediction == 0:
        output = 'Normal'
    elif prediction == 1:
        output = 'DOS'
    elif prediction == 2:
        output = 'PROBE'
    elif prediction == 3:
        output = 'R2L'
    elif prediction == 4:
        output = 'U2R'

    return render_template('index.html', output=output)

# API for results (optional)
@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = 'Unknown'
    if prediction == 0:
        output = 'Normal'
    elif prediction == 1:
        output = 'DOS'
    elif prediction == 2:
        output = 'PROBE'
    elif prediction == 3:
        output = 'R2L'
    elif prediction == 4:
        output = 'U2R'

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

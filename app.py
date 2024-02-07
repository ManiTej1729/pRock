from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import hashlib

app = Flask(__name__)
user_data_file = "users.txt"

def write_user_data(data):
    with open(user_data_file, 'w') as f:
        for user in data:
            json.dump(user, f)
            f.write('\n')  

try:
    with open(user_data_file, 'r') as f:
        lines = f.readlines()
     
        users = [json.loads(line.strip()) for line in lines if line.strip()]
        if not isinstance(users, list):
            raise ValueError("Invalid JSON data in users.txt")
except (FileNotFoundError, json.JSONDecodeError, ValueError):
    users = []

@app.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashed(password)
        existing_user = next((u for u in users if u['email'] == email), None)
        if existing_user:
            return f"User with email {email} already exists."

        user_id = len(users) + 1
        user_data = {
            'id': user_id,
            'name': name,
            'email': email,
            'password': hashed_password  
        }

        users.append(user_data)
        write_user_data(users)

        return f"Registration successful for {name} with email ID: {email}"
    
    return render_template('registration.html')

def hashed(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/user/<user_email>')
def user_details(user_email):
    email_lower = user_email.lower()

    user = next((u for u in users if u.get('email').lower() == email_lower), None)

    if user:
        hashed_password = user.get('password', '')
        user_details_with_password = user.copy()
        user_details_with_password['password'] = hashed_password
        return jsonify(user_details_with_password)
    else:
        return f"User with email {user_email} not found"

if __name__ == '__main__':
    app.run(debug=True)

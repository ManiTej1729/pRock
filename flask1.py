from flask import Flask, render_template, request, redirect, url_for
import bcrypt
import json

app = Flask(__name__)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

@app.route('/', methods=['POST','GET'])
def index():
    return render_template("login.html")

@app.route('/next', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password = hash_password(password)
        print(password) 
        user_data = {
            "name": name,
            "email": email,
            "password": password
        }
        with open('users.txt', 'a+') as file:
            json.dump(user_data, file)
            file.write("\n")
        return render_template("home.html", name=name)
    else:
        return redirect(url_for('index'))
    
@app.route('/user/<user_id>', methods=['GET'])
def find(user_id):
    with open('users.txt', 'r') as file:
        for line in file:
            stri = json.loads(line)
            if stri["name"] == user_id:
                return line
    return "User doesn't exists"
        
if __name__ == "__main__":  
    app.run(debug=True)
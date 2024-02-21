from flask import Flask, render_template, request, redirect, url_for
import bcrypt
import json


app = Flask(__name__)

salt = bcrypt.gensalt()
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

@app.route('/', methods=['POST','GET'])
def index():
    return render_template("home.html")
    
@app.route('/phin', methods=['POST', 'GET'])
def phin():
    return render_template("index.html")

@app.route('/video', methods=['POST', 'GET'])
def video():
    return render_template("video.html")

@app.route('/next/<typer>', methods=['POST', 'GET'])
def add(typer):
    # print(typer)
    if request.method == 'POST' and typer == 'signin':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password = hash_password(password)
        user_data = {
            "name": name,
            "email": email,
            "password": password
        }
        with open('users.txt', 'r') as file:
            for line in file:
                tempLine = json.loads(line)
                if tempLine['email'] == email:
                    return render_template("login.html", err="User already exists", new=typer)
        with open('users.txt', 'a+') as file:
            json.dump(user_data, file)
            file.write("\n")
        return redirect(url_for('newHome'))
    elif request.method == 'POST' and typer == 'login':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = {
            "email": email,
            "password": password
        }
        with open('users.txt', 'r') as file:
            for line in file:
                stri = json.loads(line)
                if stri["email"] == email:
                    temp = stri["password"]
                    print(password.encode('utf-8'))
                    print(temp.encode('utf-8'))
                    if bcrypt.checkpw(password.encode('utf-8'), temp.encode('utf-8')):
                        return redirect(url_for('newHome'))
            return render_template("login.html", err="Incorrect username / password", new=typer)
    return render_template("login.html", new=typer)
    
@app.route('/home2', methods=['POST', 'GET'])
def newHome():
    return render_template('home2.html')

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
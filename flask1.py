from flask import Flask, render_template, request, redirect, url_for, jsonify
import bcrypt
import json
import pymysql
import pymysql.cursors

app = Flask(__name__)

mydb = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "M@ni1234",
    database = "media_database"
)

if(mydb.open): 
    print("Connected")
    cur = mydb.cursor()
else:
    print("Falied to connect")

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
        print(name, email, password)
        cmd = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cur.execute(cmd, (name, email, password))
        mydb.commit()
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
                return jsonify(stri)
    return "User doesn't exists"
        
if __name__ == "__main__":  
    app.run(debug=True)
    
mydb.commit()
cur.close()
mydb.close()

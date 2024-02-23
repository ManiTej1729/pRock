from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import bcrypt
import json
import pymysql
import pymysql.cursors
import datetime
import jwt

app = Flask(__name__)
app.secret_key = "this_is_worlds_most_secured_secret_key"

mydb = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Vedp9565@",
    database = "media_database"
)

if(mydb.open): 
    print("Connected")
    cur = mydb.cursor()
    cur.execute("use media_database")
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
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('index'))
    return render_template("index.html")

@app.route('/video', methods=['POST', 'GET'])
def video():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('index'))
    payload = jwt.decode(token, "!@#$%", algorithms=['HS256'])
    files = request.files.getlist('image')
    print(files)
    uname = session['user_details']['username']
    print(uname)
    query = 'SELECT id FROM users WHERE username = %s'
    cur.execute(query, uname)
    fId = cur.fetchone()
    print("fid: ", fId)
    if fId:
        for img in files:
            print(img)
            filename = img.filename
            filesize = img.content_length
            fileblob = img.read()
            fidin = int(fId[0])
            print(type(fidin))
            query = f'INSERT INTO uploaded_images (user_id, image_name, fsize, bindata) VALUES ({fidin}, "{filename}", {filesize}, %s)'
            cur.execute(query, (fileblob))
            mydb.commit()
            print(fId, filename)
    return render_template("video.html")

@app.route('/next/<typer>', methods=['POST', 'GET'])
def add(typer):
    token = session.get('jwt_token')
    if token:
        return redirect(url_for('newHome'))  
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
        secret_key = '!@#$%'
        payload = {
            # 'user_id': 1,
            'username': name,
            'password': password,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        session['jwt_token'] = token
        session['user_details'] = {'username': name}
        cmd = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cur.execute(cmd, (name, email, password))
        mydb.commit()
        # return render_template()
        return redirect(url_for('newHome'))
    elif request.method == 'POST' and typer == 'login':
        print("neucwvui")
        # name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        query = 'SELECT username FROM users WHERE email = %s'

        cur.execute(query, email)
        name = cur.fetchone()
        print("name :", name[0])
        user_data = {
            "email": email,
            "password": password
        }
        with open('users.txt', 'r') as file:
            for line in file:
                stri = json.loads(line)
                if stri["email"] == email:
                    temp = stri["password"]
                    if bcrypt.checkpw(password.encode('utf-8'), temp.encode('utf-8')):
                        secret_key = '!@#$%'
                        payload = {
                            # 'user_id': 1,
                            'username': name[0],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
                        }
                        token = jwt.encode(payload, secret_key, algorithm='HS256')
                        session['jwt_token'] = token
                        session['user_details'] = {'username': name[0]}
                        print(session)
                        return redirect(url_for('newHome'))
            return render_template("login.html", err="Incorrect username / password", new=typer)
    return render_template("login.html", new=typer)
    
@app.route('/home2', methods=['POST', 'GET'])
def newHome():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('index'))
    return render_template('home2.html')

@app.route('/user/<user_id>', methods=['GET'])
def find(user_id):
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('index'))
    with open('users.txt', 'r') as file:
        for line in file:
            stri = json.loads(line)
            if stri["name"] == user_id:
                return jsonify(stri)
    return "User doesn't exists"

@app.route('/users', methods = ['POST', 'GET'])
def display():
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('index'))
    # cur.execute('SELECT * FROM users')
    # user = cur.fetchall()
    with open('users.txt') as file:
        LIST = []
        for line in file:
            lineTemp = json.loads(line)
            LIST.append(lineTemp)
        return jsonify(LIST)
    # return render_template('display.html', user=user)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     token = session.get('jwt_token')
#     if not token:
#         return redirect(url_for('index'))
#     file = request.files['file']
#     binary_data = file.read()
#     filename = file.filename
#     # sql = "INSERT INTO uploaded_images (image_name, image_data) VALUES (%s, %s)"
#     # cur.execute(sql, (filename, binary_data))
#     sql = "INSERT INTO uploaded_images (image_name, image_data) VALUES (%s, %s)"
#     cur.execute(sql, (filename, binary_data))
#     mydb.commit()
#     return ''

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('jwt_token', None)
    session.pop('user_details', None)
    return redirect(url_for('index'))
        
if __name__ == "__main__":  
    app.run(debug=True)
    
mydb.commit()
cur.close()
mydb.close()

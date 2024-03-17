import datetime
import json
import base64
import io
import cv2 as cv
import numpy as np
import bcrypt
import pymysql
import pymysql.cursors
import jwt
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Response

app = Flask(__name__)
app.secret_key = "this_is_worlds_most_secured_secret_key"
mydb = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Vedp9565@",
    database = "media_database"
)

if mydb.open:
    print("Connected")
    cur = mydb.cursor()
    cur.execute("use media_database")
else:
    print("Falied to connect")
salt = bcrypt.gensalt()
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def blob_to_base64(blob_data):
    return base64.b64encode(blob_data).decode('utf-8')

def base64_to_blob(base64_string):
    decoded_bytes = base64.b64decode(base64_string)
    blob = io.BytesIO(decoded_bytes)
    return blob.getvalue()

def resize(blob_data):
    nparr = np.frombuffer(blob_data, np.uint8)
    image = cv.imdecode(nparr, cv.IMREAD_COLOR)

    print(type(image))
    new_width = 800
    new_height = 600
    resized_image = cv.resize(image, (new_width, new_height))
    return resized_image.tostring()

not_allowed = 0

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
    # print("entered")
    files = request.files.getlist('image')
    # print("number: ", files)
    uname = session['user_details']['username']
    # print(uname)
    query = 'SELECT id FROM users WHERE username = %s'
    cur.execute(query, uname)
    fId = cur.fetchone()
    # print("fid: ", fId)
    if fId:
        for img in files:
            print(img)
            filename = img.filename
            # with open(f"{filename}", 'rb') as img:
            fileblob = img.read()
            filesize = len(fileblob)
            fidin = int(fId[0])
            # print("file size: ", filesize)
            # print("Bin data: ", fileblob)
            if filesize != 0:
                query = f'INSERT INTO uploaded_images (user_id, image_name, fsize, bindata) VALUES ({fidin}, "{filename}", {filesize}, %s)'
                cur.execute(query, (fileblob))
                mydb.commit()
                print(fId, filename)
    return render_template('home2.html')

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
        if name == 'Admin':
            return render_template("login.html", err="Please choose a different username", new=typer)
        if email == 'admin@iiit.ac.in':
            return render_template("login.html", err="Please choose a different email", new=typer)
        user_data = {
            "name": name,
            "email": email,
            "password": password
        }
        with open('users.txt', 'r') as file:
            for line in file:
                tempLine = json.loads(line)
                if tempLine['email'] == email or tempLine['name'] == name:
                    # print(tempLine)
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
        return redirect(url_for('newHome'))
    elif request.method == 'POST' and typer == 'login':
        # name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        query = 'SELECT username FROM users WHERE email = %s'

        cur.execute(query, email)
        name = cur.fetchone()
        if name == None:
            return render_template("login.html", err="User not found", new=typer)
        # print("name :", name[0])
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
                        # print(session)
                        return redirect(url_for('newHome'))
            return render_template("login.html", err="Incorrect username / password", new=typer)
    return render_template("login.html", new=typer)

@app.route('/home2', methods=['POST', 'GET'])
def newHome():
    global not_allowed
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('index'))
    uname = session['user_details']['username']
    if not_allowed == 1:
        not_allowed = 0
        return render_template('home2.html', user=uname, permission="Sorry! you don't have access to this feature")
    return render_template('home2.html', user=uname, permission="")

@app.route('/newVideo', methods = ['GET', 'POST'])
def displays():
    return render_template('video.html')

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
    global not_allowed
    token = session.get('jwt_token')
    if not token:
        return redirect(url_for('index'))
    uname = session['user_details']['username']
    if uname != 'Admin':
        not_allowed = 1
        return redirect(url_for('newHome'))
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

@app.route('/create', methods=['GET', 'POST'])
def crVid():
    img_blobs = []
    unique_uname = session['user_details']['username']
    # print(unique_uname)
    query = f'select id from users where username = "{unique_uname}"'
    # print(query)
    cur.execute(query)
    uId = cur.fetchone()
    uId = uId[0]
    # print(uId)
    query = f'select bindata from uploaded_images where user_id = {uId}'
    cur.execute(query)
    lists = cur.fetchall()
    # print(lists)
    nice_images  =[]
    for items in lists:
        img_blobs.append(items[0])
    for blobs in img_blobs:
        nice_images.append(blob_to_base64(blobs))
    # print(nice_images)

    return render_template('select.html', nice_images=nice_images)

@app.route('/slideshow', methods = ['GET', 'POST'])
def show():
    fetched_data = request.form.getlist('images')
    # print(fetched_data)
    bg_music = request.form.get('bgm')
    print(bg_music)
    audio_flag = request.form.get('music_flag')
    print(audio_flag)
    blobs = []
    for imgs in fetched_data:
        blobs.append(base64_to_blob(imgs))
    # print(blobs)
    resized_blobs = []
    for blob in blobs:
        resized_blobs.append(resize(blob))
    print(resized_blobs)
    return Response("success", 200)


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

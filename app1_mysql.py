from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="media_database"
)
cursor = mydb.cursor()
def populate_audio_library():
    audio_files = [
        ("Song 1", "Artist 1", "Pop", "Chaleya_320(PagalWorld.com.cm).mp3"),
        ("Song 2", "Artist 2", "Rock", "Heeriye_320(PagalWorld.com.cm).mp3"),
        ("Song 2", "Artist 2", "Rock", "Ram Siya Ram_320(PagalWorld.com.cm).mp3"),
        ("Song 2", "Artist 2", "Rock", "INDUSTRY-BABY---Lil-Nas-X-N-Jack-Harlow(PagalWorlld.Com).mp3"),
        ("Song 2", "Artist 2", "Rock", "Happy Birthday To You Ji(PagalWorld.com.cm).mp3"),  
        ("Song 2", "Artist 2", "Rock", "Moye-Moye(PaglaSongs).mp3"),  
    ]
    sql = "INSERT INTO audio_library (audio_name, audio_artist, audio_genre, audio_path) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, audio_files)
    mydb.commit()
def search_images(keyword):
    sql = "SELECT * FROM uploaded_images WHERE image_name LIKE %s"
    cursor.execute(sql, ('%' + keyword + '%',))
    return cursor.fetchall()


def search_audio(keyword):
    sql = "SELECT * FROM audio_library WHERE audio_name LIKE %s OR audio_genre LIKE %s"
    cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
    return cursor.fetchall()

@app.route('/search', methods=['GET'])
def search_media():
    keyword = request.args.get('keyword')
    # Call search function based on media type
    search_results = search_images(keyword)
    search_results = search_audio(keyword)
    return jsonify(search_results)

if __name__ == '__main__':``
    populate_audio_library()
    app.run(debug=True)

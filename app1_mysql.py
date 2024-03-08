import os
import mutagen
import pymysql
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="Vedp9565@",
    database="media_database"
)

cursor = mydb.cursor()

def get_song_metadata(audio_path):
    audio = mutagen.File(audio_path)
    if audio is None:
        return None, None
    if isinstance(audio, MP3):
        duration = int(audio.info.length)
    elif isinstance(audio, OggVorbis):
        duration = int(audio.info.length)
    elif isinstance(audio, FLAC):
        duration = int(audio.info.length)
    else:
        duration = None
    size = os.path.getsize(audio_path)
    return size, duration

def populate_audio_library():
    audio_files = [
        ("Chaleya_320(PagalWorld.com.cm).mp3", "Chaleya"),
        ("Heeriye_320(PagalWorld.com.cm).mp3", "Heeriye"),
        ("Happy Birthday To You Ji(PagalWorld.com.cm).mp3", "Happy Birthday To You Ji"),
        ("INDUSTRY-BABY---Lil-Nas-X-N-Jack-Harlow(PagalWorlld.Com).mp3", "Industry Baby"),
    ]
    for audio_file, audio_name in audio_files:
        size, duration = get_song_metadata(audio_file)
        if size is not None and duration is not None:
            with open(audio_file, 'rb') as f:
                bindata = f.read()
            sql = "INSERT INTO audio_library (audio_name, duration, fszie, bindata) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (audio_name, duration, size, bindata))
    mydb.commit()

populate_audio_library()

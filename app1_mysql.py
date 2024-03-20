import os
import mutagen
import pymysql
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
import psycopg2

# mydb = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="Vedp9565@",
#     database="media_database"
# )

mydb=psycopg2.connect("postgresql://ved:_fH3BfLkIHVWrNGQkG557Q@papamerepapa-9041.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/pRock?sslmode=verify-full")
cur = mydb.cursor()

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
        ("Chaleya.mp3", "Chaleya"),
        ("Heeriye.mp3", "Heeriye"),
        ("Happy Birthday To You Ji.mp3", "Happy Birthday To You Ji"),
        ("INDUSTRY-BABY.mp3", "INDUSTRY-BABY"),
    ]
    for audio_file, audio_name in audio_files:
        size, duration = get_song_metadata(audio_file)
        if size is not None and duration is not None:
            with open(audio_file, 'rb') as f:
                bindata = f.read()
            sql = "INSERT INTO audio_library (audio_name, duration, fszie, bindata) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (audio_name, duration, size, bindata))
    mydb.commit()
populate_audio_library()

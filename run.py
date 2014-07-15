from flask import Flask, request, render_template, g, jsonify
import sqlite3
import os
from pytube import YouTube
from subprocess import call
import base64
import datetime
import shutil

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "apidocs.db"),
    DEBUG=True,
    SECRET_KEY='0209012'
    )
)
app.config.from_envvar("FLASKR_SETTINGS", silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.text_factory = str
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/doconvert', methods=['POST','GET'])
def convert():

    if (request.form):
        url = request.form['url']

        yt = YouTube()
        yt.url = url
        name = yt.filename.encode("UTF-8")
        yt.filename = base64.b64encode(name)
        video = yt.get('mp4', '360p')
        video.download('/tmp/')

        mp4 = yt.filename
        mp3name = base64.b64decode(yt.filename)
        call(["ffmpeg -i /tmp/"+mp4+".mp4 -b:a 128K -vn /tmp/"+mp4+".mp3"],shell=True)


        db = get_db()
        db.execute('insert into songs (songname, base64name, dateconverted, timesdownloaded, lastdownload) values (?, ?, ?, ?, ?)',
                 [mp3name+".mp3", mp4+".mp3", datetime.datetime.now(), 1, datetime.datetime.now()])

        db.commit()

        shutil.copy2("/tmp/"+mp4+".mp3", "static/songs/"+mp3name+".mp3")
        return jsonify({'location': 1, "name":mp3name+".mp3"})

    return jsonify({'message': "There was an error. Something is missing in input."})

@app.route('/', methods=['POST', 'GET'])
def home():

    return render_template('home/index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8888, host='0.0.0.0')

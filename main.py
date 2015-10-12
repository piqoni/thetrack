from __future__ import division
from flask import Flask, render_template, request, jsonify
import soundcloud
import credentials
from pyechonest import artist

app = Flask(__name__)


# connect to Soundcloud API
client = soundcloud.Client(
    client_id=credentials.id
)


def get_artist_soundcloud_url(artist_name):
    """
    Get permalink of artist from the first result
    """
    try:
        artist = client.get('/users', q=artist_name)
    except:
        return False
    return artist[0].permalink if artist else False


def get_track_rank(plays, favorites, comments, duration):
    """
    Calculate track rank so it can be compared with other tracks.
    """
    # disregard tracks with less than 50 plays and long mixes
    if plays <= 50 or duration > 600000:
        rank = 0
    else:
        rank = (favorites / plays) + ((comments * 2) / plays)
    return rank


def build_tracks_dict(artist_permalink):
    """
    Build tracks dictionary with ranks, sort them and get the one
    with the highest rank.
    """
    track_list = {}
    tracks = client.get('/users/' + artist_permalink + '/tracks')
    for track in tracks:
        try:
            track_rank = get_track_rank(
                track.playback_count,
                track.favoritings_count,
                track.comment_count,
                track.duration
            )
            track_list[track.permalink_url] = track_rank
        except:
            pass
    return sorted(track_list.items(),
                  key=lambda item: item[1], reverse=True)[:1]


def build_player_widget(track_url):
    embed_info = client.get('/oembed', url=track_url)
    return embed_info.html


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/thetrack', methods=['POST'])
def get_track():
    if request.method == 'POST':
        search = request.form['search']
    if search:
        if search.startswith('http'):
            artist_username = search.strip("/").rsplit('/', 1)[1]
        else:
            artist_username = get_artist_soundcloud_url(search)
        if artist_username:
            track = build_tracks_dict(artist_username)
            return build_player_widget(track[0][0]) if track else 'No tracks were found'
        else:
            return 'No artist was found.'


@app.route('/similar/<artist_name>')
def get_similar_artist(artist_name):
    """
    Get similar artists using echonest API
    """
    similar_list = []
    try:
        bk = artist.Artist(artist_name)
    except:
        return "Couldn't find similar artists."
    for similar in bk.similar:
        similar_list.append(similar.name)
    return jsonify(artists=similar_list)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

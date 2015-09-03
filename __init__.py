from __future__ import division
from flask import Flask, render_template, request
import soundcloud
import credentials

app = Flask(__name__)


# API credentials
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
        artist = request.form['search']
    if artist:
        artist_link = get_artist_soundcloud_url(artist)
        if artist_link:
            track = build_tracks_dict(artist_link)
            return build_player_widget(track[0][0]) if track else 'No tracks were found'
        else:
            return 'No artist was found.'
    else:
        return False


if __name__ == '__main__':
    app.debug = True
    app.run()

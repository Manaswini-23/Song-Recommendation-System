from flask import Flask, render_template, request, jsonify
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__)

# Spotify API credentials
SPOTIFY_CLIENT_ID = '804669bc659c4ae9b1659677095e3b29'
SPOTIFY_CLIENT_SECRET = 'afa2ec1b9de84e4aa13526668a7c51e9'

# Spotify API authentication
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_latest_movie_songs(genre, mood):
    query = f'{mood} genre:{genre} soundtrack'
    tracks = []
    try:
        for offset in range(0, 100, 50):  # Fetch multiple pages of results
            results = sp.search(q=query, type='track', limit=50, offset=offset)
            tracks.extend(results['tracks']['items'])

        # Filter out duplicates and get unique tracks
        seen = set()
        unique_tracks = []
        for track in tracks:
            track_id = track['id']
            if track_id not in seen:
                seen.add(track_id)
                unique_tracks.append(track)
            if len(unique_tracks) >= 20:
                break

        return unique_tracks
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")
        return []
    except Exception as e:
        print(f"General Error: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form.get('genre').lower()
    mood = request.form.get('mood').lower()

    recommendations = get_latest_movie_songs(genre, mood)
    if recommendations:
        response = [{"name": track['name'], "artist": track['artists'][0]['name'], "url": track['external_urls']['spotify']} for track in recommendations]
        return jsonify({"success": True, "songs": response})
    else:
        return jsonify({"success": False, "message": "Sorry, we don't have recommendations for your selected genre and mood."})

if __name__ == '__main__':
    app.run(debug=True)

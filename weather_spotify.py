import spotipy
import json
import webbrowser
import urllib.request
import spotipy.util as util
from datetime import datetime

# weather_file is a variable name representing my file
with open('weather_key.txt', 'r') as weather_file:
    weather_key = weather_file.read()




with open('Spotify_keys.json', 'r') as spotify_file:
    tokens = json.load(spotify_file)

my_client_id = tokens['client_id']
my_client_secret = tokens['client_secret']
redirectURI = tokens['redirect']
username = tokens['username']

scope = "user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public"
token = util.prompt_for_user_token(username, scope, client_id=my_client_id, client_secret=my_client_secret, redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)



mood_map = {
    "Sad":["upbeat","Pop", "Dance", "Disco"],
    "Happy": ["sad","Blues", "Ballad", "Emo"],
    "Angry": ["Ambient", "Classical", "Meditation Music"],
    "Stressed": ["Meditation Music", "Lofi Hip Hop"],
    "Scared": ["Epic Orchestral", "Power Metal", "Fantasy Soundtracks"],
    "Excited": ["Lo-fi Hip Hop", "Downtempo", "Trip-Hop"],
    "Tired": ["Pop", "Rock and Roll", "Metal"],
    "Confident": ["Emo", "Indie Rock", "Folk"],
    "Focused": ["Electronic", "Noise", "IDM"],
    "Peaceful": ["Metal", "Punk", "Hardcore", "Industrial"],
    "Strong": ["Folk", "Ambient", "Drone"],
}



#get tracks fot the opposite mood
def get_opposite_mood_track(mood, num_tracks=10):
	if mood not in mood_map:
		print(f"Mood '{mood}' not found")
		return[]

	opposite_moods = mood_map[mood]
	tracks = []

	for opposite_mood in opposite_moods:
		results = sp.search(q=f"genre:{opposite_mood}", type="track", limit=10)
		tracks.extend([item["uri"]for item in results["tracks"]["items"]])

	return tracks[:num_tracks]


 #this is to genarate playlist
def get_playlist(city, mood=None):
	encoded_city = urllib.parse.quote(city)
	url = f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={city}&aqi=no"
	# sending our url to the interwebs
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	weather_json = json.loads(response.read())

	forecast = weather_json['current']['condition']['text']

	
	track_results = sp.search(q=forecast, type='track', limit=1)
	weather_tracks = [item['uri'] for item in track_results['tracks']['items']]

#get the tracks for the opposite mood if the mood is provided
	opposite_tracks = get_opposite_mood_track(mood) if mood else []
	all_tracks = weather_tracks + opposite_tracks




	playlist_name = f"Mood Playlist - {mood} ({datetime.now().date()}) - {forecast}"
	my_playlist = sp.user_playlist_create(user=username, name=playlist_name, public=True)

	sp.user_playlist_add_tracks(username, my_playlist['id'], all_tracks)
	return my_playlist['id']










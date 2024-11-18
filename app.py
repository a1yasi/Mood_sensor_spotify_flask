from flask import Flask, render_template, request
from weather_spotify import get_playlist

app = Flask(__name__)


default_city = "London"


@app.route('/', methods=['POST'])
def index_post():
	user_city = request.form.get('req_city', default_city)
	user_mood = request.form.get('mood','')


	my_playlist = get_playlist(user_city, user_mood)
	return render_template('index.html', playlist_id=my_playlist, city=user_city)




@app.route('/')
def index():
	my_playlist = get_playlist(default_city)
	return render_template('index.html', playlist_id=my_playlist, city=default_city)




from __future__ import unicode_literals
from main import SpotifyAPI, CLIENT_ID, CLIENT_SECRET, playlist_id
import webbrowser
from googleapiclient.discovery import build
import json


# -------------------------------------------------------
COUNT = 0

with open('./songs.json', 'r') as f:
	DATA = json.load(f)

api_key = ['AIzaSyCBKLRJZF30akVFf3qFoMLhPZZxcSA-II8', 'AIzaSyCxjOXVUvEk-OgrknmdVAC7HJWjYeCHwxQ', 'AIzaSyDlZ1NC0qkLZ0Etiq7qlm5rRDvtpz4YVHw']

# ------------------------------------------------------


def get_songs():
	spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
	spotify.refrech_token()
	spotify.search_playlist(playlist_id)

	with open('./songs.json', 'r') as f:
		songs = json.load(f)
	return songs


def get_song_url(song):
	ytb = build('youtube', 'v3', developerKey=api_key[COUNT])
	song_name = song['song_name']
	artist_name = song['artist_name']

	request = ytb.search().list(
		part="snippet",
		maxResults=1,
		q= f'{song_name} {artist_name}'
	)
	response = request.execute()
	videoId = response['items'][0]['id']['videoId']
	song_url = f'https://www.youtube.com/watch?v={videoId}'
	return {'song_name': song_name, 'artist_name': artist_name, 'url': song_url}


def add_urls():
	global COUNT
	songs = get_songs()
	temps = []
	while COUNT < 3:
		for song in songs[COUNT*100:(COUNT+1)*100]:
			print(song['song_name'])
			try:
				song_data = get_song_url(song)
				temps.append(song_data)
				print(song_data['url'])
			except:
				print("ERROR 404")
		COUNT += 1

	with open('./songs.json', 'w') as f :
		json.dump(temps, f, indent=4)

	return temps


def get_songs_data():
	songs = get_songs()


def open_on_browser(song):
	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
	webbrowser.get(chrome_path).open(song)


def open_all(count):
	URLS = [song['url'] for song in DATA]
	for url in URLS[count*50: (count+1)*50]:
		try:
			open_on_browser(url)
		except:
			print(url)


if __name__ == '__main__':
	# add_urls()
	open_all(4)

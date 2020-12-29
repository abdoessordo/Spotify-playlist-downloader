from __future__ import unicode_literals
from main import SpotifyAPI, CLIENT_ID, CLIENT_SECRET, playlist_id
from time import sleep
import webbrowser
import youtube_dl
from googleapiclient.discovery import build



#-------------------------------------------------------
songs = []

URLS = []

url = 'https://www.youtube.com/watch?v=RHQC4fAhcbU'

api_key = ['AIzaSyDlZ1NC0qkLZ0Etiq7qlm5rRDvtpz4YVHw', 'AIzaSyCBKLRJZF30akVFf3qFoMLhPZZxcSA-II8', 'AIzaSyCxjOXVUvEk-OgrknmdVAC7HJWjYeCHwxQ']

ytb = build('youtube', 'v3', developerKey=api_key[2])
#-------------------------------------------------------
def get_songs():
	global songs
	spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
	spotify.refrech_token()
	spotify.search_playlist(playlist_id)
	with open('./songs.txt', 'r') as f:
		songs = [line.strip() for line in f]


def get_url(song_name):
	request = ytb.search().list(
	        part="snippet",
	        maxResults=1,
	        q= song_name
	    )
	response = request.execute()
	videoId = response['items'][0]['id']['videoId']
	song_url = f'https://www.youtube.com/watch?v={videoId}'
	return song_url


def open_on_browser(song):
	chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
	webbrowser.get(chrome_path).open(song)


def open_all():
	for song in URLS[197:]:
		try:
			open_on_browser(song)
		except:
			print('song')


def download_song(song_url):
	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}
	youtube = youtube_dl.YoutubeDL(ydl_opts)
	youtube.download([song_url])


def add_URL():
	tesmpURLS = []
	for song in songs[205:]:
		try:
			url = get_url(song)
			tesmpURLS.append(url)
		except:print(song, "Didnt work")

	with open('URLS.txt', 'a') as f :
		f.write('\n')
		for url in tesmpURLS:
			if not tesmpURLS.index(url) == len(tesmpURLS) -1 :
				f.write(f'{url}\n')
			else : f.write(url) 


def get_URLS():
	global URLS
	with open('./URLS.txt', 'r') as f:
		URLS = [line.strip() for line in f]

# if __name__ == '__main__':






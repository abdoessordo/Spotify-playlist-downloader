import youtube_dl


def downlaod(video, foldername='OUTPUT/'):
	video_url = video['url']
	video_info = youtube_dl.YoutubeDL().extract_info(
		url=video_url, download=False
		)

	song_name = f"{video_info['title']}.mp3"
	if '/' in song_name:
		song_name = song_name.replace('/', '-')
	filename = f"{foldername}/{song_name}"
	options = {
		'format': 'bestaudio/best',
		'keepvideo': False,
		'outtmpl': filename,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}]
	}

	with youtube_dl.YoutubeDL(options) as ydl:
		try:
			ydl.download([video_url])
		except:
			pass


if __name__ == '__main__':
	pass

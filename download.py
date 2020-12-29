import youtube_dl

with open('../URLS.txt', 'r') as f:
	urls = [line.strip() for line in f]


def downlaod(video_url):
	video_info = youtube_dl.YoutubeDL().extract_info(
		url=video_url, download=False
		)
	filename = f"{video_info['title']}.mp3"
	print(video_info['webpage_url'])
	options = {
		'format' : 'bestaudio/best',
		'keepvideo' : False,
		'outtmpl' : filename,
		'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
        }] 
	}

	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([video_url])



if __name__ == '__main__':
	print(len(urls))
	for url in urls:
		try:
			downlaod(url)
		except:
			pass
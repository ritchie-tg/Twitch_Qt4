import os, sys, re, time, urllib, urllib2, tempfile, json

from subprocess import Popen,PIPE,STDOUT
from threading  import Thread
from Queue import Queue, Empty

def Livestreamer(streamName, oauth, cache, quality):
	def enqueue_output(out, queue):
		#only needed to read proc output in a nonblocking fashion.
		for line in iter(out.readline, b''):
			queue.put(line)
		out.close()
	call = 'streamlink --twitch-oauth-token {0} twitch.tv/{1} {2} --player "vlc --file-caching {3}" &'.format(oauth,streamName,quality,cache)
	proc = Popen(call, shell=True, stderr=STDOUT, stdout=PIPE)
	#have to use threads and queue for nonblocking stdout
	q = Queue()
	t = Thread(target=enqueue_output, args=(proc.stdout, q))
	t.daemon = True
	t.start()

	errorCode = 0
	errorComment = ''
	line = ''
	for i in range(10):
		try:
			line = q.get(timeout=1)
		except Empty:
			pass
		else: 
			pass

		if line:
			#check streamlink output for errors
			if re.search(r"'{0}' could not be found.".format(quality), line): #quality not availbale
				line = q.get(timeout=3)
				if line:
					#find next best quality
					validQualities = ['1080p60', '720p60', '720p', '480p', '360p', '160p', 'audio_only']
					b = re.search(r'Available streams: (.+)', line)
					oldQuality = quality
	
					if b:
						if b.group(1):
							for i in xrange(len(validQualities)):
								#get quality index in validQualities to be used in next loop
								if validQualities[i] == quality:
									qualityIndex = i + 1
									break
							for i in xrange(qualityIndex, len(validQualities)):
								if re.search(validQualities[i], b.group(1)):
									quality = validQualities[i]
									break
							#make sure not using same quality
							if quality != oldQuality:
								errorCode = 1
								errorComment = quality
								break
							#Livestreamer(streamName, oauth, cache, quality)
				else:
					pass
			elif re.search(r'No streams found', line): #no streamer by the name given
				errorCode = 2
				errorComment = 'Stream not found.~(Twitch_Qt)MainWindow)StreamCall)StreamLib) No stream was found with the stream name given.'
				break
			elif re.search(r'400 Client Error: (.+)', line): #bad client?
				errorCode = 3
				errorComment = 'Twitch api returned 400 client error (bad Client ID token).~(Twitch_Qt)MainWindow)StreamCall)StreamLib) The Twitch API has returned an 400 client error, which is indicative of a improper Client ID key.'
				break
			elif re.search(r'Max retries exceeded', line): #internet connection or api is down
				errorCode = 4
				errorComment = 'Check your internet connection.~Streamlink threw a "max retries exceeded" error indicating a connection issue. The internet may not be reachable or Twith.tv is expierencing issues at the momment.'
				break
			elif re.search(r'Failed to start player(.+)', line): #no media player
				errorCode = 5
				errorComment = 'Failed to open media player.~Please adjust the streamlib.py call variable in Livestreamer function to point to your media player.'
				break
			elif re.search(r'Unable to find channel', line): #no streamer by the name given
				errorCode = 6
				errorComment = 'No streamer by the name.~(Twitch_Qt)MainWindow)StreamCall)StreamLib) No stream was found with the stream name given.'
				break
			elif re.search(r'Unauthorized', line): #bad oauth
				errorCode = 7
				errorComment = 'Twitch api returned 400 client error (bad oAuth token).~(Twitch_Qt)MainWindow)StreamCall)StreamLib) The Twitch API has returned an 400 client error, which is indicative of a improper oAuth key. Make sure your token has user_read permissions and its format does NOT include the "oauth:" part.'
				break
			else:
				pass


	if not errorComment:
		return True, errorCode, errorComment
	else:
		if t:
			try:
				t.join()
			except:
				pass
		if proc:
			proc.kill()
		return False, errorCode, errorComment

def GetImage(name, address):
	imagePath = os.path.dirname(os.path.realpath(__file__)) + '/img_cache/' #for images
	imageCache = os.listdir(imagePath)
	pattern = re.compile(r'{0}'.format(name))
	hasImage = filter(pattern.match, imageCache)

	if not hasImage:
		fileName = address.split("/")[-1]
		try:
			urllib.urlretrieve(address, imagePath+name+'.'+fileName.split('.')[-1])
			return True
		except Exception as e:
			return False
	else:
		return True

def GetStreams(clientid, oauth):
	class Streamer(object):
		def __init__(self, name, game, logoPath):
			self.name = name
			self.game = game
			self.logo = logoPath
	
	###
	errorCode = 0
	errorComment = ''

	request = urllib2.Request("https://api.twitch.tv/kraken/streams/followed", headers={
		'Accept' : 'application/vnd.twitchtv.v3+json',
		'Client-ID' : clientid,
		'Authorization' : 'OAuth {0}'.format(oauth),
		})

	try:
		jsonRaw = urllib2.urlopen(request).read()
		if jsonRaw:
			jsonFile = tempfile.gettempdir() + '/twitch_followed.json'
			f = open(jsonFile, 'w') 
			f.write(jsonRaw)
			f.close()
		else:
			errorCode = 1
			errorComment = 'Failed to retrieve json data from Twitch API.~The request made to pull followed streams from the Twitch API failed. -> (streamLib.py -> jsonRaw = urllib2.urlopen(request).read())'
			return False, errorCode, errorComment
	except Exception as e:
			errorCode = 2
			errorComment = 'urllib2 request failed in streamlib.py.~{0}'.format(e)
			return False, errorCode, errorComment

	if jsonFile:
		with open (jsonFile, 'r') as data:
			jsonParsed = json.load(data)
		data.close()
		
		streams = jsonParsed['streams']
		if len(streams) > 0:
			followList = []
			for s in xrange(len(streams)):
				channel = streams[s]['channel']
				strName = channel['display_name'].lower()
				strGame = channel['game'].lower()
				strLogo = channel['logo'].lower()
				
				GetImage(strName, strLogo)
				followList.append(Streamer(strName, strGame, strLogo))
			
			return True, errorCode, followList
		else:
			errorCode = 3
			errorComment = 'Request made, but no followed streams retrieved.~Total streams:{0}'.format(len(streams))
			return False, errorCode, errorComment
	else:
		errorCode = 4
		errorComment = 'Request made, but Twitch.json file is no open.~See streamLib.py -> jsonFile variable. Check /tmp/ or /temp/ for the file twitch_followed.json and read.'
		return False, errorCode, errorComment


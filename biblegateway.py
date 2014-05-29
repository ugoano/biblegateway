import urllib2
import tweepy
import webbrowser
import re
import tinyurl
from BeautifulSoup import BeautifulSoup

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

access_token = ""
access_secret = ""

def getVerse():
	xmldata = getXml()
	(verse, link) = extractVerse(xmldata)
	verse = unescapeHTML(verse)
	if access_token == "":
		tokens = accessTwitter()
	updateTweet(verse, link, tokens)

def getXml():
	try:
		res = urllib2.urlopen("http://www.biblegateway.com/votd/get/?format=atom&version=NIV").read()
	except:
		print "Didn't work! Tell Ugo"
		raise
	return res

def extractVerse(xml):
	soup = BeautifulSoup(xml)
	entries = soup.findAll('entry')
	for entry in entries:
		title = entry.findAll('title')[0].text
		content = entry.findAll('content')[0].text
		link = entry.findAll('link')[0]["href"]
		return (title + "\n" + content, link)

def accessTwitter():
	try:
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, secure=True)
		auth.secure = True
		url = auth.get_authorization_url(True)
		req_token = auth.request_token.to_string()

		if webbrowser.open(url):
			print "Opening a url to give access to your twitter account. Then type the pin code back here..."
		else:
			print "Open the following url, then return here and type the pin code..." + "\n" + str(url)
		pin = raw_input("Pin code: ")
		
		#auth2.secure = True
		#auth2.request_token = oauth.OAuthToken.from_string(req_token)
		auth.get_access_token(pin)
		access_token = auth.access_token.key
		access_secret = auth.access_token.secret
		return (access_token, access_secret)
	except:
		print "Something went wrong here, tell Ugo"
		raise

def updateTweet(tweet, link, tokens):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, secure=True)
		auth.set_access_token(*tokens)
		api = tweepy.API(auth)
		try:
			if len(tweet) > 140:
				url = tinyurl.create_one(link)
				limit = 136 - len(url)
				tweet = tweet[:limit] + "...\"" + url
			api.update_status(tweet)
			print "Tweet updated"
		except:
			print "Something wrong with updating tweet"
			raise

def unescapeHTML(str):
	str = re.sub("&#\d+;", "", str)
	str = str.replace("&lt;", "<")
	str = str.replace("&gt;", ">")
	str = str.replace("&apos;", "'")
	str = str.replace("&quot;", "\"")
	str = str.replace("&raquo;", "\"")
	str = str.replace("&laquo;", "\"")
	str = str.replace("&rdquo;", "\"")
	str = str.replace("&ldquo;", "\"")
	str = str.replace("&rsquo;", "\'")
	str = str.replace("&lsquo;", "\'")
	str = str.replace("&ndash;", "-")
	str = str.replace("&amp;", "&")
	str = str.replace("&#39;", "'")
	str = str.replace("&nbsp;", " ")
	str = str.replace("&bull;", "")
	return str

if __name__ == "__main__":
	getVerse()

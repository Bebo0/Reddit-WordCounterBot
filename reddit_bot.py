import praw 
import string
import re
from collections import Counter

# USAGE: 
#        1) download PRAW. Follow instructions here: http://praw.readthedocs.io/en/latest/getting_started/installation.html 
#        2) in terminal, cd to folder which contains project files
#        3) type python reddit_bot.py

# VARIABLES:
subRedditName = 'cryptocurrency'
counter = Counter()

# FUNCTIONS:
def addArrToCounter(aos):
	""" Adds the occurence of all strings in given array to counter

	ArrayOfStrings -> void

	Arguments:
		aos {ArrayOfStrings} -- contains all the words to be added to counter
	"""

	for word in aos:
		if word in counter:
			counter[word] += 1
		else:
			counter[word] = 1


def authenticate():
	""" Logs us into Reddit and returns an object which allows us to interact with Reddit's API

	void -> Reddit
	"""
	print "Authenticating"
	reddit = praw.Reddit('wordcounterbot',
			user_agent = "Bebo's Word Counter")
	print "Successfully authenticated as {}".format(reddit.user.me())
	return reddit


def parseComments(reddit):
	""" Parses the first x number of comments that appear in a subreddit

	Reddit -> void
	
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""
	
	print "Parsing comments..."
	x = 1000
	for comment in reddit.subreddit(subRedditName).comments(limit=x):

		# transforms all letters of the comment body to lowercase and transforms the comment from unicode to ascii for easier readability
		strong = ''.join(comment.body).lower().encode('ascii','ignore')

		parsingHelper(strong)
	print "Successfully parsed comments!"


def parsingHelper(strong):
	""" Splits strong into individual strings then adds them to the counter 
	
	"""
	allowedSymbols = string.letters + string.digits + ' ' + '\'' + '-'
	aos = re.sub('[^%s]' % allowedSymbols,'',strong)
	aos = aos.split()
	addArrToCounter(aos)


def parsePostTitles(reddit):
	""" Parses all post titles from dateInitial to dateEnd in the given subreddit

	Reddit -> void
	
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""
	
	print "Parsing post titles..."
	dateInitial = 1514408887 #1514078600 is December 25th, 2017 9:10pm PST. Convert time to UNIX time here: https://www.unixtimestamp.com/
	dateEnd     = 1514453887  #1514265000 is December 26th, 2017 9:10pm PST

	for comment in reddit.subreddit(subRedditName).submissions(dateInitial, dateEnd):

		strong = ''.join(comment.title).lower().encode('ascii','ignore')
		parsingHelper(strong)

	print "Successfully parsed post titles!"


def runBot(reddit):
	""" Parses comments and titles
	Reddit -> void

	Parses the comments and/or titles in the given subreddit, and adds the occurence of certain strings found to counter.
		
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""
	#parseComments(reddit)
	parsePostTitles(reddit)


def main():
	
	reddit = authenticate()
	runBot(reddit)
	print counter

if __name__ == '__main__':
	main()

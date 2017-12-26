import praw 
import string
import re
from collections import Counter

# USAGE: 1) type in a Reddit username and password in the praw.ini folder
#        2) in terminal, cd to folder which contains project files
#        3) type python reddit_bot.py

# VARIABLES:
subRedditName = 'cryptocurrency'
dictionary = Counter()


def addArrToDictionary(aos):
	"""
	ArrayOfStrings -> void

	Adds all strings in given array to dictionary

	Arguments:
		aos {ArrayOfStrings} -- contains all the words to be added to dictionary
	"""

	for word in aos:
		if word in dictionary:
			dictionary[word] += 1
		else:
			dictionary[word] = 1


def authenticate():
	"""
	void -> Reddit

	Logs us into Reddit and returns an object which allows us to interact with Reddit's API
	"""
	print "Authenticating"
	reddit = praw.Reddit('wordcounterbot',
			user_agent = "Bebo's Word Counter")
	print "Successfully authenticated as {}".format(reddit.user.me())
	return reddit


def parseComments(reddit):
	"""
	Reddit -> void
	
	Parses the first x number of comments that appear in a subreddit
	
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
	"""
	Splits strong into individual strings then adds them to the dictionary 
	
	"""
	allowedSymbols = string.letters + string.digits + ' ' + '\'' + '-'
	aos = re.sub('[^%s]' % allowedSymbols,'',strong)
	aos = aos.split()
	addArrToDictionary(aos)


def parsePostTitles(reddit):
	"""
	Reddit -> void
	
	Parses all post titles from dateInitial to dateEnd in the given subreddit
	
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""
	
	print "Parsing post titles..."
	dateInitial = 1514178600 #December 25th, 2017 9:10pm PST. Convert time to UNIX time here: https://www.unixtimestamp.com/
	dateEnd     = 1514265000 #December 26th, 2017 9:10pm PST

	for comment in reddit.subreddit(subRedditName).submissions(dateInitial, dateEnd):

		strong = ''.join(comment.title).lower().encode('ascii','ignore')
		parsingHelper(strong)

	print "Successfully parsed post titles!"


def runBot(reddit):
	"""
	Reddit -> void

	Parses the comments and titles in the given subreddit, and adds certain strings found to dictionary.
		
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""
	parseComments(reddit)
	parsePostTitles(reddit)


def main():
	
	reddit = authenticate()
	runBot(reddit)
	print dictionary

if __name__ == '__main__':
	main()

import praw 
import string
import re
import time
from collections import Counter
from Authenticator import authenticate

# USAGE: 
#        1) download PRAW. Follow instructions here: http://praw.readthedocs.io/en/latest/getting_started/installation.html 
#        2) in terminal, cd to folder which contains project files
#        3) type python WordCounterBot.py

class WordCounterBot:
	TIME_NOW         = int(time.time()) # epoch (UTC) time
	TIME_24HOURS_AGO = int(time.time()) - 86400
	TIME_7DAYS_AGO   = int(time.time()) - 86400*7

	reddit = authenticate() #authenticate called here so that only 1 authentication occurs even if multiple objects are instantiated

	# CONSTRUCTOR:
	def __init__(self, subredditname):
		"""constructs a WordCounterBot object
		
		Arguments:
			subredditname {string} -- the subreddit being parsed
		"""
		self.subRedditName = subredditname
		self.counter = Counter() 

    # FUNCTIONS:
	def addArrToCounter(self, aos):
		""" Adds the occurence of all strings in given array to counter

		ArrayOfStrings -> void

		Arguments:
			aos {ArrayOfStrings} -- contains all the words to be added to counter
		"""

		for word in aos:
			if word in self.counter:
				self.counter[word] += 1
			else:
				self.counter[word] = 1


	def authenticate():
		""" Logs us into Reddit and returns an object which allows us to interact with Reddit's API

		void -> Reddit
		"""
		print "Authenticating"
		reddit = praw.Reddit('wordcounterbot',
				user_agent = "Bebo's Word Counter")
		print "Successfully authenticated as {}".format(reddit.user.me())
		return reddit


	def parseComments(self, reddit):
		""" Parses the first x number of comments that appear in a subreddit

		Reddit -> void
		
		Arguments:
			reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
		"""
		
		print "Parsing comments..."
		x = 1000
		for comment in reddit.subreddit(self.subRedditName).comments(limit=x):

			# transforms all letters of the comment body to lowercase and transforms the comment from unicode to ascii for easier readability
			strong = ''.join(comment.body).lower().encode('ascii','ignore')

			self.parsingHelper(strong)
		print "Successfully parsed comments!"


	def parsingHelper(self, strong):
		""" Splits strong into individual strings then adds them to the counter 
		
		"""
		allowedSymbols = string.letters + string.digits + ' ' + '\'' + '-'
		aos = re.sub('[^%s]' % allowedSymbols,'',strong)
		aos = aos.split()
		self.addArrToCounter(aos)


	def parsePostTitles(self, reddit):
		""" Parses all post titles from dateInitial to dateEnd in the given subreddit

		Reddit -> void
		
		Arguments:
			reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
		"""
		
		print "Parsing post titles..."

		for comment in reddit.subreddit(self.subRedditName).submissions(TIME_7DAYS_AGO, TIME_NOW):

			strong = ''.join(comment.title).lower().encode('ascii','ignore')
			self.parsingHelper(strong)

		print "Successfully parsed post titles!"


	def runBot(self, reddit):
		""" Parses comments and titles
		Reddit -> void

		Parses the comments and/or titles in the given subreddit, and adds the occurence of certain strings found to counter.
			
		Arguments:
			reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
		"""
		self.parseComments(reddit)
		# self.parsePostTitles(reddit)


def main():

	bot = WordCounterBot('cryptocurrency')
	bot.runBot(WordCounterBot.reddit)
	print bot.counter

if __name__ == '__main__':
	main()
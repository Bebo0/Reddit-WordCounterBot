import praw 
import string
import re
from collections import Counter

## USAGE: 1) type in a Reddit username and password in the praw.ini folder
##        2) in terminal, cd to folder which contains project files
##        3) type python reddit_bot.py

subRedditName = 'cryptocurrency'
dictionary = Counter()


"""
void -> Reddit

Logs us into Reddit and returns an object which allows us to interact with Reddit's API
"""
def authenticate():
	print "Authenticating"
	reddit = praw.Reddit('wordcounterbot',
			user_agent = "Bebo's Word Counter")
	print "Successfully authenticated as {}".format(reddit.user.me())
	return reddit


"""
ArrayOfStrings -> void

Adds all strings in given array to dictionary

Arguments:
	aos {ArrayOfStrings} -- contains all the words to be added to dictionary
"""
def addArrToDictionary(aos):

	for word in aos:
		if word in dictionary:
			dictionary[word] += 1
		else:
			dictionary[word] = 1



def parseComments(reddit):
	"""
	Reddit -> void
	
	Parses the first x number of comments that appear in a subreddit
	
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""
	
	print "Parsing comments..."
	x = 5
	for comment in reddit.subreddit(subRedditName).comments(limit=x):

		# transforms all letters of the comment body to lowercase and transforms the comment from unicode to ascii for easier readability
		strong = ''.join(comment.body).lower().encode('ascii','ignore')

		parsingHelper(strong)
	print "Successfully parsed comments!"

def parsePostTitles(reddit):
	"""
	Reddit -> void
	
	Parses all post titles from dateInitial to dateEnd in the given subreddit
	
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""
	
	print "Parsing post titles..."

	for comment in reddit.subreddit(subRedditName).submissions(1513998000, 1514150308):

		strong = ''.join(comment.title).lower().encode('ascii','ignore')
		parsingHelper(strong)

	print "Successfully parsed post titles!"



def parsingHelper(strong):
	"""
	Splits strong into individual strings then adds them to the dictionary 
	
	"""
	allowedSymbols = string.letters + string.digits + ' ' + '\'' + '-'
	aos = re.sub('[^%s]' % allowedSymbols,'',strong)
	aos = aos.split()
	addArrToDictionary(aos)





def run_bot(reddit):
	"""
	Reddit -> void

	Parses the comments and titles in the given subreddit, and split them up into invidivual.
		
	Arguments:
		reddit {Reddit} -- [the Reddit object that allows us to interact with Reddit's API]
	"""

	
	
	parseComments(reddit)
	parsePostTitles(reddit)
	#print "Parsing comments..."
	#for comment in reddit.subreddit('cryptocurrency').submissions(1513998000, 1514150308):

		#strong = ''.join(comment.title).lower().encode('ascii','ignore')

		#print "Parsing comments..."
	# for comment in reddit.subreddit(subRedditName).comments(limit=10000):

	# 	strong = ''.join(comment.body).lower().encode('ascii','ignore')

	# 	allow = string.letters + string.digits + ' ' + '\'' + '-'
	# 	lol = re.sub('[^%s]' % allow,'',strong)

	# 	lol = lol.split()

	# 	for word in lol:
	# 		if word in dictionary:
	# 			dictionary[word] += 1
	# 		else:
	# 			dictionary[word] = 1

	print dictionary
	#print type (dictionary)


def main():
	
	reddit = authenticate()
	run_bot(reddit)

if __name__ == '__main__':
	main()

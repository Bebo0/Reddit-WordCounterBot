import praw 
import time
import string
import re
from collections import Counter

## USAGE: 1) type in a Reddit username and password in the praw.ini folder
##        2) in terminal, cd to folder which contains project files
##        3) type python reddit_bot.py

def authenticate():
	print "Authenticating"
	reddit = praw.Reddit('wordcounterbot',
			user_agent = "Bebo's Word Counter")
	print "Successfully authenticated as {}".format(reddit.user.me())
	return reddit

def run_bot(reddit):
	dictionary = Counter()
	print "Parsing comments..."
	#for comment in reddit.subreddit('cryptocurrency').submissions(1513998000, 1514150308):

		#strong = ''.join(comment.title).lower().encode('ascii','ignore')

		#print "Parsing comments..."
	for comment in reddit.subreddit('cryptocurrency').comments(limit=10000):

		strong = ''.join(comment.body).lower().encode('ascii','ignore')

		allow = string.letters + string.digits + ' ' + '\'' + '-'
		lol = re.sub('[^%s]' % allow,'',strong)

		lol = lol.split()

		for word in lol:
			if word in dictionary:
				dictionary[word] += 1
			else:
				dictionary[word] = 1
	print dictionary
	#print type (dictionary)


def main():
	reddit = authenticate()
	run_bot(reddit)

if __name__ == '__main__':
	main()
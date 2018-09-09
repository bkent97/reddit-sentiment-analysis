import praw
import time
import sentiment_mod as s
from praw.models import MoreComments
from nltk.tokenize import word_tokenize

def analysis(keywords, filename, subreddit):
	r = praw.Reddit(client_id='Wy91R-3FGeonsA',
		client_secret='kIshI9kHV3kQkF4A7rCgwVcJ6Pg',
		user_agent='my user agent')
	
	sub = r.subreddit(subreddit)
	comments_judged = 0
	comments_read = 0
	for comment in sub.stream.comments():
		words = word_tokenize(comment.body)
		if not keywords:
			match = 1
		else:
			match = 0

		comments_read += 1
		if len(comment.body) < 20:
			continue
		for word in words:
			#throw out comments with sarcasm
			if word.lower() == "[removed]":
				match = 0
			if word.lower() == "\s" or word.lower() == "/s":
				match = 0
				break

			#check for matches with keywords
			if match == 0:
				for key in keywords:
					if word.lower() == key.lower():
						match = 1
						break 
			

		#judge the comment
		if match == 1:
			print("here")
			comments_judged += 1
			tude = s.sentiment(comment.body)[0]
			conf = s.sentiment(comment.body)[1]
			if tude == "pos":
				print("positive comment detected: ", comment.body)
				f = open(filename, "a")
				f.write("pos\n")
				f.close()

			elif tude == "neg":
				print("negative comment detected: ", comment.body)
				f = open(filename, "a")
				f.write("neg\n")
				f.close()


#analysis(["trump", "potus", "donald", "donnie"], ".txt", 'all')

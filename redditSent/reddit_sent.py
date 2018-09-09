import praw
import time
import sentiment_mod as s
from nltk.tokenize import word_tokenize
from praw.models import MoreComments
from nltk.corpus import wordnet as wn

def analysis(keywords, filename, subreddit):
	r = praw.Reddit(client_id='Wy91R-3FGeonsA',
		client_secret='kIshI9kHV3kQkF4A7rCgwVcJ6Pg',
		user_agent='my user agent')
	sub = r.subreddit(subreddit)
	total_comments = 0
	comments_read = 0
	for post in sub.top('all'):
#		print(post.permalink)
		filepath = "attitudes/"
		filepath += filename
#		f = open(filepath, "a")
		for comment in post.comments:
#		print(dir(comment))
			if isinstance(comment, MoreComments):
				continue
			
			comments_read += 1
			words = word_tokenize(comment.body)
			found = 0
			adj = 0
			for word in words:
				#look for a match in keywords
				if found == 0:
					for key in keywords:
						if word.lower() == key.lower():
							found = 1

				#looking for adjectives
#				if len(wn.synsets(word)) > 0:
				#	print(word)
#					pos = wn.synsets(word)[0].pos()
#					if pos == 's' or pos == 'a':
#						adj = 1

				#if sarcasm, should toss the comment
				if word.lower() == "\s" or word.lower() == "\\s":
					found = 0
					adj = 0
					break


			#found a keyword, judge the comment
			if found == 1:	
				conf = (s.sentiment(comment.body)[1])
				attitude = str(s.sentiment(comment.body)[0])
				if conf > 0.75:
					total_comments += 1
					if attitude == "pos":
#						print("Detected positive comment: " + str(comment.body) + "\n" + "confidence: " + str(conf) + "\n")
						f = open(filepath, "a")
						f.write("pos\n")
						f.close()
					else:
#						print("Detected negative comment: " + str(comment.body) + "\n" + "confidence: " + str(conf) + "\n")
						f = open(filepath, "a")
						f.write("neg\n")
						f.close()

			# do the same for all replies to comment
			for reply in comment.replies:
				if isinstance(comment, MoreComments):
					continue
	
				comments_read += 1
				words = word_tokenize(comment.body)
				found = 0
				adj = 0
				for word in words:
					#check for adjective
#					if len(wn.synsets(word)) > 0:
#						pos = wn.synsets(word)[0].pos()
#						if pos == 's' or pos == 'a':
#							adj = 1

					#if sarcasm, should toss the comment
					if word.lower() == "\s" or word.lower() == "\\s":
						found = 0
						adj = 0
						break

					#look for a match in keywords
					if found == 0:
						for key in keywords:
							if word.lower() == key.lower():
								found = 1

				#found a keyword, judge the comment
				if found == 1:	
					conf = (s.sentiment(comment.body)[1])
					attitude = str(s.sentiment(comment.body)[0])
					if conf > 0.75:
						total_comments += 1
						if attitude == "pos":
#							print("Detected positive comment: " + str(comment.body) + "\n" + "confidence: " + str(conf) + "\n")
							f = open(filepath, "a")
							f.write("pos\n")
							f.close()
						else:
#							print("Detected negative comment: " + str(comment.body) + "\n" + "confidence: " + str(conf) + "\n")
							f = open(filepath, "a")
							f.write("neg\n")
							f.close()


#		f.close()
	print("Total number of comments judged: ", total_comments)
	print("Total number of comments read: ", comments_read)

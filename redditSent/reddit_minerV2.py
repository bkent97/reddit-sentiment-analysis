import praw
from praw.models import MoreComments

r = praw.Reddit(client_id='Wy91R-3FGeonsA',
                client_secret='kIshI9kHV3kQkF4A7rCgwVcJ6Pg',
                user_agent='my user agent')

sub = r.subreddit('politics')
f = open("negative_comments.txt", "w")
count = 0
for post in sub.hot(limit = 100):
	if count >= 5000:
		break
	post.comments.replace_more(limit=None)
	for comment in post.comments.list():
		line = (str(comment.body)).rstrip() + "\n"
		f.write(line)
		count += 1

f.close()

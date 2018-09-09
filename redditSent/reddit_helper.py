import reddit_comment_stream as r
import sys, getopt
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

def animate(i):
	with open(filepath, 'r') as f:
		results = f.read()
	lines = results.split('\n')
	
	xar = []
	yar = []
	
	x = 0
	y = 0
	for line in lines:
		x += 1
		if "pos" in line:
			y += 1
		elif "neg" in line:
			y -= 0.3

		xar.append(x)
		yar.append(y)

	ax1.clear()
	ax1.plot(xar, yar)

def main(argv):
	try:
		filename = argv[0]
		subreddit = argv[1]
		keywords = argv[2]
	except:
		print("python reddit_helper.py <filename> <subreddit> <keywords,separated,by,commas>(or type 'NONE' for no keywords)")
		sys.exit(2)
	
	#get keys into a list
	if keywords == "NONE":
		keywords = []
	else:
		keywords = keywords.split(',')
	
	#complete filepath
	global filepath
	filepath = "attitudes/"
	filepath += filename

	#start a separate thread so comment stream can run in the background
	sentiment_thread = threading.Thread(target=r.analysis, args=[keywords,filepath,subreddit])
	sentiment_thread.start()

	#check if file exists, if not, then create it
	try:
		f = open(filepath, "r")
		f.close()
	except:
		f = open(filepath, "w")
		f.close()
	
	style.use("ggplot")
	plt.rc('font', family='Arial')
	fig = plt.figure()
	global ax1
	ax1 = fig.add_subplot(1,1,1)

	#live graph
	ani = animation.FuncAnimation(fig, animate, interval=1000)
	plt.show()


if __name__ == "__main__":
   main(sys.argv[1:])

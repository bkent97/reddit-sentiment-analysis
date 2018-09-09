import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import praw

style.use("ggplot")

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i, filepath):
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
			y -= 0.5
		
		xar.append(x)
		yar.append(y)

	ax1.clear()
	ax1.plot(xar, yar)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
				

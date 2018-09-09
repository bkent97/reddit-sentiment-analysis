import sentiment_mod as s

f = open("amazon06-25.txt", "r")
lines = f.read().splitlines()
correct = 0
incorrect = 0
for line in lines:
	if len(line) > 30:
		rating = line[:3]
		review = line[4:]
		print("Score: ", rating, '\n', review, '\n', s.sentiment(review)[0])
		if s.sentiment(review)[0] == 'pos' and float(rating) > 3.0:
			correct += 1

		if s.sentiment(review)[0] == 'pos' and float(rating) < 3.0:
			incorrect += 1

		if s.sentiment(review)[0] == 'neg' and float(rating) > 3.0:
			incorrect += 1

		if s.sentiment(review)[0] == 'neg' and float(rating) < 3.0:
			correct += 1


print("Correct: ", correct, '\n', "Incorrect: ", incorrect)

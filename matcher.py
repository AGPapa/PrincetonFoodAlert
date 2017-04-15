# reads in dhall options and matches with users
import sys

food = 'red peppers'

while True:
	s = sys.stdin.readline();
	if not s: break
	tokens = s.split('\t')
	wordsDhall = tokens[3].lower().strip().split(' ')
	wordsFood = food.split(' ')
	match = 0
	count = 0
	for wordFood in wordsFood:
		count = count + 1
		for wordDhall in wordsDhall:
			if wordFood == wordDhall:
				match = match + 1
				break
	if match == count:
		print(s)
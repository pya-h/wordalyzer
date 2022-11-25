import pandas as pd

class Word:
	S = []
	def __init__(self, id, post_id, word, writer, dateofbirth):
		self.id = id
		self.post_id = post_id
		self._ = word
		self.writer = writer
		self.dateofbirth = dateofbirth
		Word.S.append(self)

	@staticmethod
	def Load(filename):
		file = pd.read_csv(filename)
		for row in file:
			id = row.iloc[0]
			post_id = row.iloc[1]
			msg  = row.iloc[2]
			writer = row.iloc[3]
			reader = row.iloc[4]
			date = row.iloc[5]
			words = msg.split()
			#filter signs
			for word in words:
				Word(word, id, post_id, writer, date)

	def count(self, mark = '#', date = None, writer = None, post_id = None):
		# write additional code for filtering conditions
		statistics = dict()
		for word in Word.S:
			if word._[0] == mark:
				actual_word = word._[1:]
				statistics[actual_word] = statistics[actual_word] + 1 if actual_word in statistics else 1
		return statistics

	def sort_stats(self, statistics):
		return sorted(statistics.items(), key = lambda kv: (kv[1], kv[0]))
#	sorted_dict = {dictionary_keys[i]: sorted(
#    dict.values())[i] for i in range(len(dictionary_keys))}

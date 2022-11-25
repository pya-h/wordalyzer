class Word:
	S = []
	def __init__(self, id, post_id, word, owner, date, likes=None, location=None):
		self.id = id
		self.post_id = post_id
		self._ = word
		self.owner = owner
		self.date = date
		self.likes = likes
		self.location = location
		Word.S.append(self)

	@staticmethod
	def count(mark = '#', date = None, owner = None, post_id = None):
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

	def __str__(self) -> str:
		return self._

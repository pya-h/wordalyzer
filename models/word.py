def find_max(collection):
	if not collection:
		return (None, None)
	max_idx = list(collection.keys())[0] if type(collection) is dict else 0
	max_value = collection[max_idx]
	for key in collection:
		if collection[key] > collection[max_idx]:
			max_idx = key
			max_value = collection[key]

	return (max_idx, max_value)

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
	def iterations(mark = '#', date = None, owner = None, post_id = None):
		# write additional code for filtering conditions
		iters = dict()
		for word in Word.S:
			if word._[0] == mark:
				actual_word = word._[1:]
				iters[actual_word] = iters[actual_word] + 1 if actual_word in iters else 1
		return iters


	@staticmethod
	def most_used(limit = None):
		word_stats = Word.iterations()
		if not limit or limit <= 0:
			return word_stats
		temp = word_stats.copy()
		filtered_keys = []
		for i in range(limit):
			k, v = find_max(temp)
			if not k and not v:
				break
			filtered_keys.append(k)
			del temp[k] # remove most used to find the limit floor

		if not temp:
			return word_stats
		i, limit_floor = find_max(temp)
		words = list(filter(lambda idx: idx in filtered_keys, word_stats))
		return (words, list(map(lambda word: word_stats[word], words)))


	def __str__(self) -> str:
		return self._


	def sort_stats(self, statistics):
		return sorted(statistics.items(), key = lambda kv: (kv[1], kv[0]))
#	sorted_dict = {dictionary_keys[i]: sorted(
#    dict.values())[i] for i in range(len(dictionary_keys))}


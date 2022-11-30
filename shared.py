
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


def find_diffrenet(previous, current):
	if previous and current:
		for i, x in enumerate(previous):
			if x != current[i]:
				return i

	return -1

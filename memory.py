class memory:
	
	def __init__(self, dict, memoryLimit = 50):
		self.keys = list(dict.keys())
		self.values = list(dict.values())
		self.memoryLimit = memoryLimit
	
	def __len__(self):
		return len(self.keys)
	
	def __getitem__(self, key):
		for i in range(0, len(self)):
			if (self.keys[i] == key):
				return self.values[i]
		raise KeyError()
	
	def __setitem__(self, key, value):
		i = 0
		while (i < len(self.keys) and key != self.keys[i]):
			i += 1
		if (i >= len(self.keys)):
			self.keys = [key] + self.keys[:(min(len(self), self.memoryLimit) - 1)]
			self.values = [value] + self.values[:(min(len(self), self.memoryLimit) - 1)]
		else:
			self.keys = [key] + self.keys[:i] + self.keys[(i + 1):]
			self.values = [value] + self.values[:i] + self.values[(i + 1):]
	
	def clear(self):
		self.keys.clear()
		self.values.clear()
	
	def keys(self):
		return self.keys
	
	def values(self):
		return self.values
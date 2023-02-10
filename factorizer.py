from math import log, sqrt
from .memory import memory

class factorizer:
	
	"""
	
	Create a factorizer object
	
	Parameters
	----------
	memoryLimit : int, default = 50
		The number of factorizations to keep in memory for recall
	
	"""
	def __init__(self, memoryLimit = 50):
		# A memory object of the last [memoryLimit] factored numbers and their factors
		self.memory = memory({}, memoryLimit = memoryLimit)
		# The maximum allowed number of factorizations to remember
		self.memoryLimit = memoryLimit
		# The last number factored
		self.last = 0
		# The factors of the last number factored
		self.factors = []
	
	def addMemory(self):
		"""
		
		An internal function to modify a factorizer object's memory
		
		Add the last factored number to the memory of the object and ensure
		that the total count of factorizations remembered is under the
		memoryLimit
		
		"""
		self.memory[self.last] = self.factors
	
	def clearMemory(self):
		"""
		
		An internal function to clear a factorizer object's memory
		
		Clear the memory of the object (just in case)
		
		"""
		self.memories.clear()
	
	def factor(self, n):
		"""
		
		Factor a positive integer
		
		Given a positive integer n, factor returns a list of tuples of the form
		(p, a) where p is a prime divisor of n and a is the order of p in n
		
		Parameters
		----------
		n : int
			A positive integer
		
		Return
		------
		A list of tuples representing the prime factors and their respective
		orders of n
		
		"""
		if (n != self.last):
			self.last = n
			try:
				return self.memory[n]
			except KeyError:
				c = n
				k = 2
				factors = []
				while (k <= sqrt(c)):
					if (c % k == 0):
						factors.append(k)
						c = c // k
					else:
						k += 1
				if (c != 1):
					factors.append(c)
				i = 0 
				while (i < len(factors)):
					self.factors.append([factors[i], 0])
					while (i < len(factors) and factors[i] == self.factors[-1][0]):
						self.factors[-1][1] += 1
						i += 1
		self.addMemory()
		return self.factors
	
	def check(n):
		"""
		
		Check a value n to ensure that it is a positive integer
		
		Parameters
		----------
		n : any type
			An input of any type (any non-numerical input could raise an exception)
		
		Return
		------
		Either the input value or its integer conversion
		
		"""
		n = int(n)
		if (n < 1 or type(n) is not int):
			raise ValueError(f"Value {n} is invalid (n must be a positive integer)")
		return n
	
	def euPhi(self, n):
		"""
		
		Computes Euler's Phi Function valued at n
		
		Parameters
		----------
		n : int
			A positive integer
		
		Return
		------
		The number of integers less than n which are coprime with n (a and b
		are considered coprime if gcd(a, b) = 1)
		
		"""
		if (factorizer.check(n) == 1):
			return 1
		self.factor(n)
		e = 1
		for prime, power in self.factors:
			e *= (prime ** (power - 1) * (prime - 1))
		return e
	
	def rad(self, n):
		"""
		
		Computes the integer radical of a number
		
		Parameters
		----------
		n : int
			A positive integer
		
		Return
		------
		The product of the unique prime factors of n
		
		"""
		if (factorizer.check(n) == 1):
			return 1
		self.factor(n)
		r = 1
		for p, a in self.factors:
			r *= p
		return r
	
	def divs(self, n):
		"""
		
		Computes the number of divisors a number has
		
		Parameters
		----------
		n : int
			A positive integer
		
		Return
		------
		The number of divisors of n between 1 and n (inclusive)
		
		"""
		if (factorizer.check(n) == 1):
			return 1
		self.factor(n)
		d = 1
		for p, a in self.factors:
			d *= (a + 1)
		return d
	
	def divSum(self, n):
		"""
		
		Computes the sum of a number's divisors
		
		Parameters
		----------
		n : int
			A positive integer
		
		Return
		------
		The sum of the positive integer divisors of n
		
		"""
		if (factorizer.check(n) == 1):
			return 1
		self.factor(n)
		ds = 1
		for p, a in self.factors:
			ds *= (p ** (a + 1) - 1) // (p - 1)
		return ds
	
	def mobius(self, n):
		"""
		
		Computer the mobius function at n
		
		Parameters
		----------
		n : int
			A positive integer
		
		Return
		------
		0 if n is not squarefree, -1 if n has an odd number of factors, 1 if n
		has an even number of factors
		
		"""
		self.factor(n)
		if (not self.isSquareFree(n)):
			return 0
		return 1 - 2 * (len(self.factors) % 2)
	
	def isSquareFree(self, n):
		"""
		
		Checks if a number is squarefree
		
		Parameters
		----------
		n : int
			A positive integer
		
		Return
		------
		True if n has no square divisors, false if not
		
		"""
		self.factor(n)
		for p, a in self.factors:
			if (a % 2 == 0):
				return False
		return True
	
	def ord(self, a, m):
		"""
		
		Find the order of a modulo m
		
		Parameters
		----------
		a : int
			A positive integer
		m : int
			A positive integer
		
		Return
		------
		The smallest positive integer k such that a^k is congruent to 1 modulo m
		
		"""
		if (self.gcd(a, m) == 1):
			return None
		for k in range(1, m):
			if ((a ** k) % m == 1):
				return k
	
	def carmichael(self, n):
		"""
		
		Calculate the Carmichael function at n
		
		Parameters
		----------
		n : int
			A positive integer
		
		Returns
		-------
		The lowest k such that a^k is congruent to 1 modulo n for any a coprime with n
		
		"""
		self.factor(n)
		if (factorizer.check(n) == 1):
			return 1
		return self.lcm(*[(p ** (a - 1) * (p - 1)) for p, a in self.factors])
	
	def digitSum(self, n, b = 10):
		"""
		
		Calculate the sum of the digits of n
		
		Parameters
		----------
		n : int
			A positive integer
		b : int, default = 10
			A positive integer representing the base for the digits used
		
		Return
		------
		The sum of the digits of n in base b
		
		"""
		t = 0
		m = int(log(n) / log(b))
		for i in range(0, m + 1):
			t += b ** (m - i) * (n % b ** (i + 1))
		return (n + (b - 1) * t) // b ** (m + 1)
	
	def gcd(self, *args):
		"""
		
		Find the greatest common divisor of the inputs
		
		Parameters
		----------
		*args : int
			Any (non-zero) number of positive integers
		
		Return 
		------
		The largest positive integer which divides all the inputs
		
		"""
		nArgs = len(args)
		if (nArgs == 0):
			raise TypeError("No input provided")
		elif (nArgs == 1):
			return args[0]
		elif (nArgs > 2):
			return self.gcd(args[-1], self.gcd(*args[0:-1]))
		a, b = max(args[0], args[1]), min(args[0], args[1])
		a, b = b % a, a
		while (a > 0):
			a, b = b % a, a
		return b
	
	def lcm(self, *args):
		"""
		
		Find the lowest common multiple of the input integers
		
		Parameter
		----------
		*args : int
			Any (non-zero) number of positive integers
		
		Return 
		------
		The least positive integer which is a multiple of all the inputs
		
		"""
		nArgs = len(args)
		if (len(args) == 0):
			raise TypeError("No input provided")
		p = 1
		for n in args:
			p *= n
		return p // (self.gcd(*args) ** (nArgs - 1))

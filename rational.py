from .factorizer import factorizer

class rational:
	def __init__(self, num, den):
		"""
		
		Create a new rational object
		
		Parameters
		----------
		num : int
			An integer to use as the numerator
		den : int
			An integer to use as the denominator
		
		"""
		if (type(num) is not int):
			raise TypeError("Numerator must be an integer")
		elif (type(den) is not int):
			raise TypeError("Denominator must be an integer")
		elif (den == 0):
			raise ZeroDivisionError("Denominator cannot be 0")
		self.num = num
		self.den = den
		self.f = factorizer()
		self.simplify()
	
	"""
	
	Magic methods
	
	"""
	def __add__(self, q):
		try:
			l = self.f.lcm(self.den, q.den)
			a = self.num * l // self.den + q.num * l // q.den
			if (a % l == 0):
				return a // l
			return rational(self.num * l // self.den + q.num * l // q.den, l)
		except AttributeError:	
			a = self.num + q * self.den
			if (a % self.den == 0):
				return a // self.den
			return rational(a, q.den)
	
	def __call__(self):
		return self.num / self.den
	
	def __div__(self, q):
		return rational(self.num * q.den, self.den * q.num)
	
	def __mul__(self, q):
		a = self.num * q.num
		b = self.den * q.den
		if (a % b == 0):
			return a // b
		return rational(a, b)
	
	def __neg__(self):
		return rational(-self.num, self.den)
	
	def __pow__(self, q):
		if (type(q) is float and q != 0):
			if ((self.num ** q) ** (1 / q) != self.num):
				raise ValueError(f"{self.num}^{q} is not a rational number")
			elif ((self.den ** q) ** (1 / q) != self.den):
				raise ValueError(f"{self.num}^{q} is not a rational number")
			elif (q > 0):
				return rational(int(self.num ** q), int(self.den ** q))
			else:
				return rational(int(self.den ** q), int(self.num ** q))
		elif (type(q) is rational):
			return self ** q()
		elif (type(q) is int):
			if (q >= 0):
				return rational(self.num ** q, self.den ** q)
			elif (q < 0):
				return rational(self.den ** q, self.num ** q)		
	
	def __radd__(self, q):
		return self + q
	
	def __rmul__(self, q):
		return self * q
	
	def __rsub__(self, q):
		try:
			l = self.f.lcm(self.den, q.den)
			a = -self.num * l // self.den + q.num * l // q.den
			if (a % l == 0):
				return a // l
			return rational(-self.num * l // self.den + q.num * l // q.den, l)
		except AttributeError:	
			a = -self.num + q * self.den
			if (a % self.den == 0):
				return a // self.den
			return rational(a, q.den)
	
	def __rtruediv__(self, q):
		try:
			a = self.den * q.num
			b = self.num * q.den
			if (a % b == 0):
				return a // b
			return rational(a, b)
		except AttributeError:
			return rational(self.num, self.den * q)
	
	def __str__(self):
		return f"{self.num}/{self.den}"
	
	def __sub__(self, q):
		try:
			l = self.f.lcm(self.den, q.den)
			a = self.num * l // self.den - q.num * l // q.den
			if (a % l == 0):
				return a // l
			return rational(self.num * l // self.den - q.num * l // q.den, l)
		except AttributeError:
			a = self.num - q * self.den
			if (a % self.den == 0):
				return a // self.den
			return rational(a, q.den)
	
	def __truediv__(self, q):
		try:
			a = self.num * q.den
			b = self.den * q.num
			if (a % b == 0):
				return a // b
			return rational(a, b)
		except AttributeError:
			return rational(self.num, self.den * q)
	
	"""
	
	Internal methods
	
	"""
	
	def inv(self):
		return rational(self.den, self.num)
	
	def simplify(self):
		d = self.f.gcd(self.num, self.den)
		self.num = self.num // d
		self.den = self.den // d
		return self

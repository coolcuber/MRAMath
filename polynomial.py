from .checkErrors import isType
from copy import copy

class polynomial:

	def __init__(self, *args, var = 'x', pMod = None, nMod = None, **kwargs):
		"""

		Create a polynomial object

		Parameters
		----------
		*args : list
			The objects used to initialize the polynomial.  Should have between
			0 and 2 values. If blank, a polynomial of value zero will be
			created.  If only one argument is given, it should be either a
			number or a string.  A number will create a constant polynomial of
			that value and a string will be parsed into the polynomial it
			describes.  If containing two values, those values should either
			both be numbers or lists.  If both are numbers, the first and
			second will be treated as the constant and power, respectively, of
			a single-term polynomial.  If both are equal length lists of
			numbers, the first and second lists will be treated as
			corresponding lists of the polynomial's constants and exponents.
		var : char, default = 'x'
			The string representing the variable to be used in string creation.
			Set to "x" by default.
		**kwargs : dictionary list
			Any number of objects of the form 'name = value' representing any
			constant values that appear in the input string.

		"""
		nArgs = len(args)
		if (nArgs == 0):
			self.constList = [0]
			self.powerList = [1]
		elif (nArgs == 1):
			if (isType(args[0], str)):
				self.setPoly(polynomial.fromString(args[0], var = var, **kwargs))
			elif (isType(args[0], int, float)):
				self.constList = [args[0]]
				self.powerList = [0]
			else:
				raise ValueError("Not enough or incorrect keywords given")
		elif (nArgs == 2):
			self.setPoly(polynomial.fromLists(args[0], args[1]))
		else:
			raise ValueError(f"Unknown input: {args}")
		self.nTerms = len(self.powerList)
		self.simplify()
		self.var = var
		self.pMod = pMod
		self.nMod = nMod
	
	"""
	
	The magic methods for polynomials.  For details, visit
	https://docs.python.org/3/reference/datamodel.html
	
	"""
	
	def __add__(self, p):
		if (polynomial.isNumType(p)):
			p = polynomial(p)
		elif (isType(p, str)):
			p = polynomial.fromString(p)
		s = self.copy()
		for const, power in p:
			s.append([const, power])
		return s

	def __call__(self, x):
		if (polynomial.isNumType(x)):
			t = 0
		else:
			t = polynomial(0, 0)
		for const, power in self:
			t += x ** power * const
		return t

	def __copy__(self):
		p = polynomial(0)
		p.constList = self.constList[:]
		p.powerList = self.powerList[:]
		p.nTerms = self.nTerms
		p.var = self.var
		p.degree = self.degree
		return p

	def __contains__(self, term):
		self.simplify()
		const, power = term
		i = self.powerList.find(power)
		return i != -1 and self.constList[i] == const

	def __eq__(self, p):
		if (self.getMaxTerm() != p.getMaxTerm() or self.nTerms != p.nTerms or self.var != p.var):
			return False
		for const, power in self:
			pConst = p.getConstant(power)
			if (pConst == None or pConst != const):
				return False
		return True

	def __floordiv__(self, p):
		if (isType(p, int, float)):
			if (p == 0):
				raise ZeroDivisionError("Cannot divide by zero")
			for i in range(0, self.nTerms):
				self[i][0] /= p
		elif (isType(p, polynomial)):
			if (self.degree < p.degree):
				return polynomial(0)
			# self.degree >= p.degree
			a = copy(self)
			b = p
			t = polynomial(0)
			while (a.degree >= b.degree):
				aConst, aPower = a.getMaxTerm()
				bConst, bPower = b.getMaxTerm()
				d = polynomial(aConst / bConst, aPower - bPower)
				t += d
				a -= d * b
			return t

	def __getitem__(self, i):
		return self.constList[i], self.powerList[i]

	def __iadd__(self, p):
		if (polynomial.isNumType(p)):
			p = polynomial(p)
		for const, power in p:
			self.append([const, power])
		return self

	def __imul__(self, p):
		self = self * p
		return self

	def __ipow__(self, power):
		self = self ** power
		return self

	def __isub__(self, p):
		if (polynomial.isNumType(p)):
			p = polynomial(p)
		for const, power in p:
			self.append([-const, power])
		return self

	def __iter__(self):
		self.i = 0
		return self

	def __len__(self):
		return self.nTerms

	def __mod__(self, m):
		if (polynomial.isNumType(m)):
			p = polynomial(0)
			for const, power in self:
				p.append([const % m, power])
			return p
		elif (isType(m, polynomial)):
			a = copy(self)
			b = m
			while (a.degree >= b.degree):
				aConst, aPower = a.getMaxTerm()
				bConst, bPower = b.getMaxTerm()
				d = polynomial(aConst // bConst, aPower - bPower)
				a -= b * d
			return a

	def __mul__(self, p):
		if (polynomial.isNumType(p)):
			p = polynomial(p, 0)
		r = polynomial(0, 0)
		for pConst, pPower in p:
			for selfConst, selfPower in self:
				r = r + polynomial(pConst * selfConst, pPower + selfPower)
		r.simplify()
		return r

	def __ne__(self, p):
		return not (self == p)

	def __neg__(self):
		n = polynomial(0, 0)
		for const, power in self:
			n = n + polynomial(-const, power)
		return n

	def __next__(self):
		self.i += 1
		if (self.i == len(self) + 1):
			raise StopIteration
		return self[self.i - 1]

	def __pow__(self, p):
		if (type(p) is not int or p < 0):
			raise ArithmeticError("Polynomial objects can only be raised to positive integer powers")
		r = polynomial(1, 0)
		if (self.pMod != None):
			for i in range(0, p):
				r = ((r * self) % self.pMod) % self.nMod
		for i in range(0, p):
			r = r * self
		r.simplify()
		return r

	def __radd__(self, p):
		return self + p

	def __rsub__(self, p):
		return -self + p

	def __rmul__(self, p):
		return self * p

	def __rpow__(self, p):
		if (self.isConstant()):
			return p ^ self(0)
		raise ArithmeticError(f"Cannot raise {p} to a polynomial power")

	def __repr__(self):
		return f"<polynomial: {self.__str__()}>"

	def __str__(self):
		self.order()
		if (self.nTerms == 0):
			return "0"
		str = f"{self.constList[0]}"
		if (self.powerList[0] != 0):
			str += f"{self.var}^{self.powerList[0]}"
		for i in range(1, self.nTerms):
			str = f"{self.constList[i]}{self.var}^{self.powerList[i]} + " + str
		return str

	def __sub__(self, p):
		if (polynomial.isNumType(p)):
			p = polynomial(p)
		elif (isType(p, str)):
			p = polynomial.fromString(p)
		s = self.copy()
		for const, power in p:
			s.append([-const, power])
		return s
	
	"""
	
	Functions for internal use.  None of these are really meant to be used
	outside of this class
	
	"""

	def append(self, term):
		const, power = term
		if (const == 0):
			return
		i = 0
		maxI = len(self)
		while (i < maxI and power != self[i][1]):
			i += 1
		if (i >= maxI):
			self.checkDegree(power)
			self.constList.append(const)
			self.powerList.append(power)
			self.nTerms += 1
			if (self.nTerms == 2 and self.constList[0] == 0):
				self.pop(0)
		else:
			self.constList[i] += const
			if (self.constList[i] == 0):
				self.pop(i)
				if (power == self.degree):
					# Find next lowest degree
					self.checkDegree()
			

	def checkConsts(self, consts):
		if (type(consts) is list):
			self.constList = consts
		elif (polynomial.isNumType(consts)):
			self.constList = [consts]
		else:
			raise TypeError("consts must be either a list or a number")

	def checkDegree(self, *args):
		nArgs = len(args)
		if (nArgs == 0):
			# no arguments given, finds degree from scratch
			pMax = 0
			for i in range(0, self.nTerms):
				pMax = max(pMax, self[i][1])
			self.degree = pMax
		elif (nArgs == 1):
			# a single (power) argument is given
			self.degree = max(self.degree, args[0])

	def checkPowers(self, powers):
		if (type(powers) is list):
			self.powerList = powers
		elif (type(powers) is int):
			self.powerList = [powers]
		else:
			raise TypeError("powers must be either a list or an integer")

	def simplify(self):
		# Construct final lists
		i = 0
		while (i < self.nTerms):
			const, power = self[i]
			if (not polynomial.isNumType(const)):
				raise TypeError("All constant values must be numbers")
			if (not isType(power, int)):
				raise TypeError("All exponents must be integers")
			if (const == 0):
				# If constant term is zero, leave it out
				i += 1
				continue
			k = 0
			# Find if power is already in powerList
			while (k < i and self.powerList[k] != power):
				k += 1
			if (k < i and self[k][1] == power):
				# If power has already appeared in powerList
				self.constList[k] += const
				self.pop(i)
				continue
			i += 1
		# Check for (and remove) zeros in constList
		i = 0
		maxPower = 0
		while (i < self.nTerms):
			if (self[i][0] == 0 and self.powerList[0] > 0):
				self.pop(i)
				continue
			if (self[i][1] > maxPower):
				maxPower = self[i][1]
			i += 1
		self.degree = maxPower

	def checkValues(self):
		for i in range(0, self.nTerms):
			if (not polynomial.isNumType(self.constList[i])):
				raise TypeError(f"Constant at position {i} ({self.constList[i]}) in constant list is not a number")
			elif (type(self.powerList[i]) is not int):
				raise TypeError(f"Value at position {i} ({self.powerList[i]}) in power list is not a number")

	def clear(self):
		self.constList = [0]
		self.powerList = [0]
		self.nTerms = 1
		self.degree = 0

	def copy(self):
		p = polynomial(self.constList[:], self.powerList[:], var = self.var)
		return p
	
	@staticmethod
	def fromLists(consts, powers):
		p = polynomial()
		p.checkConsts(consts)
		p.checkPowers(powers)
		if (len(p.constList) != len(p.powerList)):
			raise ValueError("Amounts of constants and powers do not match")
		return p

	@staticmethod
	def fromString(str, var = 'x', **kwargs):
		numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		opDict = {
			'+': [0, lambda a, b: a + b],
			'-': [0, lambda a, b: a - b],
			'*': [1, lambda a, b: a * b],
			'%': [1, lambda a, b: a % b],
			'^': [2, lambda a, b: a ** b],
			'(': [-1],
			')': [-1]
			}
		values = []
		ops = []
		numChar = lambda c: c in numList or c == '.'
		pars = 0
		i = 0
		valueLast = False
		while i < len(str):
			c = str[i]
			# Do not check valueLast if one of these characters
			if (c == ')'):
				pars -= 1
				if (pars < 0):
					raise ValueError("Mismatched parentheses")
				op = ops.pop()
				while (op != '('):
					values.append(opDict[op][1](values.pop(-2), values.pop()))
					op = ops.pop()
				valueLast = True
				i += 1
				continue
			elif (c in opDict.keys() and opDict[c][0] >= 0):
				opLast = True
				while (len(ops) > 0 and opDict[c][0] <= opDict[ops[-1]][0]):
					values.append(opDict[ops.pop()][1](values.pop(-2), values.pop()))
				ops.append(c)
				valueLast = False
				i += 1
				continue
			elif (c == ' '):
				i += 1
				continue
			# Deal with valueLast
			if (valueLast):
				while (len(ops) > 0 and 1 <= opDict[ops[-1]][0]):
					values.append(opDict[ops.pop()][1](values.pop(-2), values.pop()))
				ops.append('*')
			# Proceed
			if (numChar(c)):
				num = ""
				decimal = False
				while (numChar(c) and i < len(str)):
					if (c == '.'):
						if (decimal):
							raise ValueError("Two decimals detected")
						decimal = True
					num += c
					i += 1
					if (i < len(str)):
						c = str[i]
				i -= 1
				if (decimal):
					values.append(float(num))
				else:
					values.append(int(num))
			elif (c in [x[0] for x in kwargs]):
				arg = c
				while (i < len(str) and arg not in kwargs and arg in [x[0:len(arg)] for x in kwargs]):
					i += 1
					arg += str[i]
				if (arg in kwargs):
					v = kwargs[arg]
					if (not polynomial.isNumType(v)):
						raise ValueError(f"Constant values must be numbers ({v} is not a number)")
					values.append(kwargs[arg])
				else:
					raise ValueError(f"Unknown input ({arg})")
			elif (c == var):
				values.append(polynomial(1, 1))
			elif (c == '('):
				pars += 1
				ops.append(c)
				i += 1
				valueLast = False
				continue
			else:
				raise ValueError(f"Unknown character detected: {c}")
			valueLast = True
			i += 1
		while (len(ops) > 0):
			values.append(opDict[ops.pop()][1](values.pop(-2), values.pop()))
		return values.pop()
	
	@staticmethod
	def expMod(p, a, m):
		t = polynomial(1)
		for i in range(0, a):
			t *= p
			t = t % m
		return t

	def getConstant(self, power):
		i = 0
		while (i < self.nTerms and self[i][1] != power):
			i += 1
		if (i >= self.nTerms):
			return None
		else:
			return self[i][0]

	def getMaxTerm(self):
		return max(self, key = lambda x: x[1])

	def isConstant(self):
		return not self.nTerms > 1 and (self.nTerms == 0 or self[0][1] == 0)

	@staticmethod
	def isNumType(o):
		return isType(o, int, float)

	def order(self):
		# only works on simplified polynomials
		newConstList = []
		newPowerList = []
		for i in range(0, len(self)):
			k = 0
			cCur, pCur = self[i]
			while (k < len(newPowerList) and pCur > newPowerList[k]):
				k += 1
			if (k >= len(newPowerList)):
				newConstList.append(cCur)
				newPowerList.append(pCur)
			else:
				# pCur < newPowerList[k]
				newConstList.insert(k, cCur)
				newPowerList.insert(k, pCur)
		self.constList = newConstList
		self.powerList = newPowerList

	# DOES NOT CHECK DEGREE
	def pop(self, i):
		const = self.constList.pop(i)
		power = self.powerList.pop(i)
		self.nTerms -= 1
		if (self.nTerms == 0):
			self.constList = [0]
			self.powerList = [0]
			self.nTerms = 1
		return const, power

	def removeZeros(self):
		i = 0
		while (i < self.nTerms):
			if (self.constList[i] == 0):
				self.pop(i)
			else:
				i += 1
		if (self.nTerms == 0):
			self.clear()

	def setPoly(self, p):
		self.constList = p.constList
		self.powerList = p.powerList
		self.nTerms = p.nTerms
		self.var = p.var

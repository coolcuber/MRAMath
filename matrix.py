# REMEMBER MATRICES START AT [1, 1]

class matrix:
	
	def __init__(self, values):
		"""
		
		Create a matrix object
		
		Parameters
		----------
		values : list
			A list of equal length lists of values
		
		"""
		self.nRows = len(values)
		self.nCols = len(values[0])
		self.values = values
	
	"""
	
	Magic methods
	
	"""
	
	def __add__(self, m):
		if (self.dim() != m.dim()):
			raise ValueError("Incorrect dimensions")
		return matrix([[(self[i, j] + m[i, j]) for j in range(1, self.nCols + 1)] for i in range(1, self.nRows + 1)])	
	
	def __eq__(self, m):
		if (self.nRows != m.nRows or self.nCols != m.nCols):
			return False
		for i in range(1, self.nRows + 1):
			for j in range(1, self.nCols + 1):
				if (self[i, j] != m[i, j]):
					return False
		return True
	
	def __getitem__(self, index):
		return self.values[index[0] - 1][index[1] - 1]
	
	def __len__(self):
		return self.nRows * self.nCols
	
	def __mul__(self, m):
		try:
			if (self.nCols != m.nRows):
				raise ValueError("Multiplication error")
			r = matrix.zero(self.nRows, m.nCols)
			for i in range(1, self.nRows + 1):
				for j in range(1, m.nCols + 1):
					r[i, j] = sum([self[i, n] * m[n, j] for n in range(1, self.nCols + 1)])
		except AttributeError:
			r = matrix.zero(self.nRows, self.nCols)
			for i in range(1, self.nRows + 1):
				for j in range(1, self.nCols + 1):
					r[i, j] = m * self[i, j]
		return r
	
	def __neq__(self, m):
		return not self == m
	
	def __pow__(self, a):
		if (not isinstance(a, int)):
			raise TypeError("Matrices can only be raised to integer powers")
		if (a < 0):
			return self.inv() ** -a
		r = matrix.identity(self.nCols)
		for i in range(0, a):
			r = r * self
		return r
	
	def __rmul__(self, m):
		return m * self
	
	def __rtruediv__(self, m):
		return m * self ** -1
	
	def __setitem__(self, index, value):
		self.values[index[0] - 1][index[1] - 1] = value
	
	def __str__(self):
		ret = ""
		maxDigs = [len(str(max(*col, key = lambda x: len(str(x))))) for col in self.getColumns()]
		for i in range(1, self.nRows + 1):
			ret += "|"
			for j in range(1, self.nCols + 1):
				a = self[i, j]
				digs = len(str(a))
				ret += f"{(maxDigs[j - 1] - len(str(a))) * ' '}{a}" + (' ' if (j < self.nCols) else '')
			ret += '|\n'
		return ret
	
	def __truediv__(self, m):
		return self * m ** -1
	
	"""
	
	Internal methods.  None of these are meant to be used outside of this class.  Those that are are defined at the module level as well.
	
	"""
	
	def adjoint(self):
		return matrix.fromFunction(self.nRows, self.nCols, lambda i, j: (-1) ** (i + j) * matrix.det(self.reduced(i, j)))
	
	def addColumn(self, col):
		self.nCols += 1
		for i in range(0, self.nRows):
			self.values[i].append(col[i])
	
	def addRow(self, row):
		self.nRows += 1
		self.values += [[row]]
	
	def det(self):
		if (len(self) == 1):
			return self[1, 1]
		t = 0
		for j in range(1, self.nCols + 1):
			t -= (-1) ** j * self[1, j] * self.reduced(1, j).det()
		return t
	
	def dim(self):
		return self.nRows, self.nCols
	
	def getColumn(self, col):
		return [self[i, col] for i in range(1, self.nRows + 1)]
	
	def getColumns(self):
		return [[self.getColumn(j)] for j in range(1, self.nCols + 1)]
	
	def getRow(self, i):
		return self.values[i - 1]
	
	def getRows(self):
		return self.values
	
	def inv(self):
		d = self.det()
		if (d == 0):
			raise ValueError("Tried to invert a non-invertible matrix")
		return self.adjoint() / d
	
	def isSquare(self):
		return self.nCols == self.nRows
	
	def reduced(self, row, col):
		ret = matrix.zero(self.nRows - 1, self.nCols - 1)
		for i in range(1, self.nRows):
			for j in range(1, self.nCols):
				ret[i, j] = self[i + (i >= row), j + (j >= col)]
		return ret
	
	def transpose(self):
		return matrix(self.getColumns)
	
	@staticmethod
	def identity(n):
		"""
		
		Create an identity matrix
		
		Parameter
		---------
		n : int
			A positive integer
		
		Return
		------
		An nxn identity matrix
		
		"""
		i = matrix.zero(n, n)
		for k in range(1, n + 1):
			i[k, k] = 1
		return i
	
	@staticmethod
	def zero(rows, cols):
		"""
		
		Create a zero matrix
		
		Parameter
		---------
		n : int
			A positive integer
		
		Return
		------
		An nxn matrix of zeros
		
		"""
		return matrix([[0] * cols for i in range(0, rows)])
	
	@staticmethod
	def dot(a, b):
		if (len(a) != len(b)):
			raise ValueError("Vectors must be of equal lengths")
		return sum(a[i] * b[i] for i in range(0, len(a)))
	
	@staticmethod
	def fromFunction(m, n, func):
		"""
		
		Create an nxm matrix using func as a guideline
		
		Parameters
		----------
		m : int
			A positive integer
		n : int
			A positive integer
		func : lambda
			A function of two variables
		
		Return
		------
		An mxn matrix A such that A[i, j] = func(i, j)
		
		"""
		return matrix([[func(i, j) for j in range(1, n + 1)] for i in range(1, m + 1)])

def det(m):
	return m.det()

def adjoint(m):
	return m.adjoint()

def transpose(m):
	m.transpose()

def isSquare(m):
	return m.isSquare()
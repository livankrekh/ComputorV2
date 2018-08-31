import parser
import re

class Var:

	def __init__(self):
		self.val = None
		self.polish = None
		self.type = -1
		self.x = None

	def isVal(self):
		return self.type == 0

	def isFunc(self):
		return self.type == 1

	def isMatrix(self):
		return type(self.val) is list

	def createFunc(self, eq, arg, ALL):
		self.type = 1
		self.x = arg.lower()

		self.val = self.transform(eq, ALL)
		self.polish = parser.infixToPostfix(self.val).split()

	def createVal(self, eq, ALL):
		self.type = 0

		self.polish = parser.infixToPostfix(self.transform(eq, ALL)).split()
		
		if (self.isVal()):
			self.val = parser.resolveInfix(self.polish)

	def resolve(self, arg=None):
		if (self.isVal()):
			return self.val
		if (self.isFunc()):
			copy = self.polish[:] if (type(self.polish) is list) else []

			if (type(arg) is list):
				raise Exception('Error: cannot include matrix or vector as a argument of function')

			if (arg == None):
				return None

			if (type(arg) is complex):
				copy = self.val[:].replace(self.x, " ( " + (str(arg.real) + " + " if (arg.real != 0) else '')  + str(arg.imag) + "i ) ")
				copy = parser.infixToPostfix(copy).split()
			else:
				for i, elem in enumerate(copy):
					if (elem == self.x):
						copy[i] = str(arg)

			return parser.resolveInfix(copy)

	def show(self):
		if (self.isVal()):
			if (self.isMatrix()):
				for elem in self.val:
					print('\033[1m\033[32m', elem, '\033[0m', sep='')
				return
			if type(self.val) is complex:
				return print('\033[1m\033[32m', self.val.real, ' + ', self.val.imag, 'i', '\033[0m', sep='')

			return print('\033[1m\033[32m', str(self.val), '\033[0m', sep='')

		if (self.isFunc()):
			return print('\033[1m\033[32m', self.val, '\033[0m', sep='')

	def transform(self, expr, ALL):
		regex = re.compile('(\-?\d*\.?\d*i?)?([^i\d\W]+)(\(.*\))?')
		regex_n = re.compile('\-?\d+\.?\d*(i|j)?')
		regex_i = re.compile('(\-?\d+\.?\d*)(i)(\+|\-)?(\-?\d+\.?\d*)')

		varies = regex.findall(expr)

		for var in varies:
			koff_str = var[0]
			var_str = var[1]
			arg_str = var[2][1:-1]

			res = None

			if (var_str.lower() not in ALL and var_str.lower() != self.x and var_str != 'i' and var_str != 'j'):
				print('Warning: Undefined variable \'', var_str, '\'. Ignored!', sep='')
				expr = expr.replace(koff_str + var_str + var[2], '', 1)
			elif (var_str.lower() == self.x and arg_str == ''):
				koff = '-1' if koff_str == '-' else koff_str
				expr = expr.replace(koff_str + var_str + var[2], (koff + ' * ( ' + self.x + ' ) ') if (koff != '') else self.x, 1)
			else:
				if (var_str.lower() in ALL and ALL[var_str.lower()].isVal()):
					res = ALL[var_str.lower()].resolve()
					koff = '-1' if koff_str == '-' else koff_str
					if (ALL[var_str.lower()].isMatrix()):
						res = "["
						for row in ALL[var_str.lower()].val:
							res += str(row) + ";"
						res += "]"
					expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + str(res) + ' ) ' if (koff != '') else str(res)), 1)
				elif (var_str.lower() in ALL and ALL[var_str.lower()].isFunc()):
					if (arg_str == '' and self.isVal()):
						res = ALL[var_str.lower()]
						self.type = 1
						self.x = res.x

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + res.val + ' ) ' if (koff != '') else res.val), 1)
					elif (arg_str == '' and self.isFunc()):
						res = ALL[var_str.lower()]
						new_val = res.replace(res.x, self.x)

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + new_val + ' ) ' if (koff != '') else new_val), 1)
					elif (arg_str != ''):
						res_var = Var()
						res_var.createVal(arg_str, ALL)
						if (res_var.isMatrix()):
							raise Exception('Error: cannot include a matrix as a argument in function \'', var_str, '\'')
						res = ALL[var_str.lower()].resolve(res_var.val)

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + str(res) + ' ) ' if (koff != '') else str(res)), 1)
				else:
					print('Warning: Can\'t include variable', var_str)

		expr = parser.toNormalForm(expr)

		return expr

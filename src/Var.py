from src.parser import *
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

	def isComplex(self):
		return type(self.val) is complex

	def createFunc(self, eq, arg, ALL):
		self.type = 1
		self.x = arg.lower()

		if (eq.count('(') != eq.count(')')):
			raise Exception('Error: no open or end bracket!')
		if (eq.count('[') != eq.count(']')):
			raise Exception('Error: no open or end square bracket!')

		self.val = self.transform(eq, ALL)
		self.polish = infixToPostfix(self.val).split()

	def createVal(self, eq, ALL):
		transformed = ''
		self.type = 0

		if (eq.count('(') != eq.count(')')):
			raise Exception('Error: no open or end bracket!')
		if (eq.count('[') != eq.count(']')):
			raise Exception('Error: no open or end square bracket!')

		transformed = self.transform(eq, ALL)
		self.polish = infixToPostfix(transformed).split()

		if (self.isVal()):
			self.val = resolveInfix(self.polish, ALL)
		else:
			self.val = transformed

	def resolve(self, arg=None):
		if (self.isVal()):
			return self.val
		if (self.isFunc()):
			copy = self.polish[:] if (type(self.polish) is list) else []

			if (arg == None):
				return None

			if (type(arg) is complex):
				copy = self.val[:].replace(self.x, " ( " + (str(arg.real) + " + " if (arg.real != 0) else '')  + str(arg.imag) + "i ) ")
				copy = infixToPostfix(copy).split()
			else:
				for i, elem in enumerate(copy):
					if (elem == self.x):
						if (type(arg) is list):
							copy[i] = matrixToStr(arg)
						else:
							copy[i] = str(arg)

			return resolveInfix(copy)

	@staticmethod
	def include_complex(number):
		ret = ""

		if (type(number) is complex):
			ret += str(number.real) + " + " + str(number.imag) + "i"

		return ret

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
		regex = re.compile('(\-?\d*\.?\d*i?)?([^\d\W]+)(\(.*?\))?')
		regex_n = re.compile('\-?\d*\.?\d*(i|j)?')
		regex_i = re.compile('(\-?\d*\.?\d*)(i)(\+|\-)?(\-?\d+\.?\d*)')

		expr = toNormalForm(expr)

		varies = regex.findall(expr)

		for var in varies:
			koff_str = var[0]
			var_str = var[1]
			arg_str = var[2][1:-1]

			res = None

			if (var_str.lower() not in ALL and var_str.lower() != self.x and var_str != 'i'):
				print('\033[1mWarning: Undefined variable \'', var_str, '\'. Ignored!\033[0m', sep='')
				expr = expr.replace(koff_str + var_str + var[2], '', 1)
			elif (var_str.lower() == self.x and arg_str == ''):
				koff = '-1' if koff_str == '-' else koff_str
				expr = expr.replace(koff_str + var_str + var[2], (" " + koff + ' * ( ' + self.x + ' ) ') if (koff != '') else self.x, 1)
			else:
				if (var_str.lower() in ALL and ALL[var_str.lower()].isVal()):
					res = ALL[var_str.lower()].resolve()
					koff = '-1' if koff_str == '-' else koff_str
					if (ALL[var_str.lower()].isMatrix()):
						res = matrixToStr(ALL[var_str.lower()].val)
					elif (ALL[var_str.lower()].isComplex()):
						res = " ( " + Var.include_complex(ALL[var_str.lower()].val) + " ) "
					expr = expr.replace(koff_str + var_str + var[2], " " + koff + (' * ( ' + str(res) + ' ) ' if (koff != '') else str(res)), 1)
				elif (var_str.lower() in ALL and ALL[var_str.lower()].isFunc()):
					res = ALL[var_str.lower()]
					if ((arg_str == '' or (arg_str == res.x and res.x not in ALL)) and self.isVal()):
						self.type = 1
						self.x = res.x

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], " " +  koff + (' * ( ' + res.val + ' ) ' if (koff != '') else res.val), 1)
					elif ((arg_str == '' or (arg_str == res.x and res.x not in ALL)) and self.isFunc()):
						new_val = res.val.replace(res.x, self.x)

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], " " + koff + (' * ( ' + new_val + ' ) ' if (koff != '') else new_val), 1)
					elif (arg_str != ''):
						res_var = Var()
						res_var.createVal(arg_str, ALL)
						res = ALL[var_str.lower()].resolve(res_var.val)
						if (type(res) is complex):
							res = " ( " + str(res.real) + " + " + str(res.imag) + 'i ) '
						elif (type(res) is list):
							res = matrixToStr(res)

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], " " + koff + (' * ( ' + str(res) + ' ) ' if (koff != '') else str(res)), 1)
				else:
					if (var_str != 'i'):
						print('\033[1mWarning: Can\'t include variable', var_str, '\033[0m')

		expr = toNormalForm(expr)

		return expr

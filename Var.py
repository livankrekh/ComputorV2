import parser
import re

class Var:

	def __init__(self):
		self.val = None
		self.polish = None
		self.type = -1
		self.x = None

	def createFunc(self, eq, arg, ALL):
		self.type = 1
		self.x = arg.lower()

		print('ARG -------> ', self.x)

		self.val = self.transform(eq, ALL)
		print('TRANSFORM --->', self.val)
		self.polish = parser.infixToPostfix(self.val).split()
		print('Postfix --->', self.polish)

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

			if (arg == None):
				return None

			print('Copy', copy)

			for i, elem in enumerate(copy):
				if (elem == self.x):
					copy[i] = str(arg)

			print('Copy2', copy)

			return parser.resolveInfix(copy)


	def show(self):
		if (self.isVal()):
			if self.val is complex:
				return print(self.val.real, ' + ', self.val.imag, 'i', sep='')

			return print(str(self.val))

		if (self.isFunc()):
			return print(self.val)

	def isVal(self):
		return self.type == 0

	def isFunc(self):
		return self.type == 1

	def isMatrix(self):
		return self.type == 2

	def isScalar(self):
		return self.type == 3

	def transform(self, expr, ALL):
		regex = re.compile('(\-?\d*\.?\d*)?([^\d\W]+)(.*)?')
		regex_n = re.compile('\-?\d+\.?\d*(i|j)?')
		regex_i = re.compile('(\-?\d+\.?\d*)(i)(\+|\-)?(\-?\d+\.?\d*)')

		varies = regex.findall(expr)

		for var in varies:
			koff_str = var[0]
			var_str = var[1]
			arg_str = var[2].replace('(', '').replace(')', '')

			res = None

			if (var_str.lower() not in ALL and var_str.lower() != self.x):
				print('Warning: Undefined variable \'', var_str, '\'. Ignored!', sep='')
			elif (var_str.lower() == self.x and arg_str == ''):
				koff = '-1' if koff_str == '-' else koff_str
				expr = expr.replace(koff_str + var_str + var[2], koff + ' * ( ' + self.x + ' ) ' if (koff != '') else self.x)
			else:
				if (var_str.lower() in ALL and ALL[var_str.lower()].isVal()):
					res = ALL[var_str.lower()].resolve()
					koff = '-1' if koff_str == '-' else koff_str
					expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + str(res) + ' ) ' if (koff != '') else str(res)))
				elif (var_str.lower() in ALL and ALL[var_str.lower()].isFunc()):
					if (arg_str == '' and self.isVal()):
						res = ALL[var_str.lower()]
						self.type = 1
						self.x = res.x

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + res.val + ' ) ' if (koff != '') else res.val))
					elif (arg_str == '' and self.isFunc()):
						res = ALL[var_str.lower()]
						new_val = res.replace(res.x, self.x)

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + new_val + ' ) ' if (koff != '') else new_val))
					elif (arg_str != ''):
						res_var = Var()
						res_var.createVal(arg_str, ALL)
						res = ALL[var_str.lower()].resolve(res_var.val)

						koff = '-1' if koff_str == '-' else koff_str
						expr = expr.replace(koff_str + var_str + var[2], koff + (' * ( ' + str(res) + ' ) ' if (koff != '') else str(res)))
				else:
					print('Warning: Can\'t include variable', var_str)

		expr = expr.replace(' ', '')
		expr = expr.replace('^', ' ^ ')
		expr = expr.replace('/', ' / ').replace('*', ' * ').replace('+', ' + ').replace('%', ' % ').replace('-', ' - ')
		expr = expr.replace('   ', ' ').replace('  ', ' ').replace('* - ', '* -').replace('+ - ', '+ -')
		expr = expr.replace('/ - ', '/ -').replace('% - ', '% -').replace('^ - ', '^ -').replace('- - ', '- -')
		expr = expr.replace('(', ' ( ').replace(')', ' ) ')

		print('EXPR =', expr)

		return expr

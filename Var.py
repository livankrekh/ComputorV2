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
		self.x = arg

		self.val = self.transform(eq, ALL)
		print('TRANSFORM --->', self.val)
		self.polish = parser.infixToPostfix(self.val).split()
		print('Postfix --->', self.polish)

	def createVal(self, eq, ALL):
		self.type = 0

		self.polish = parser.infixToPostfix(self.transform(eq, ALL)).split()
		self.val = parser.resolveInfix(self.polish)

	def resolve(self, arg=None):
		if (self.isVal()):
			return self.val
		if (self.isFunc()):
			copy = self.polish.copy if (self.polish is list) else []

			if (arg == None or type(arg) is not (float or int)):
				return None

			for i, elem in enumerate(copy):
				if (elem == self.x):
					copy[i] = str(arg)

			return parser.resolveInfix(copy)


	def show(self):
		if (self.isVal()):
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
		regex = re.compile('([\-\d]\d*[^\d\W]+|\-?\d+\.\d+[^\d\W]+)')
		regex_koff = re.compile('\-?\d*(\.\d+)?')
		regex_arg = re.compile('(\-?\d*(\.\d+)?)?' + re.escape(self.x)) if (self.x != None) else ''
		var_regex = re.compile('[^\d\W]+')
		expr = expr.replace(' ', '')
		expr = expr.replace('(', ' ( ').replace(')', ' ) ').replace('^', ' ^ ')
		expr = expr.replace('/', ' / ').replace('*', ' * ').replace('+', ' + ').replace('%', ' % ').replace('-', ' - ')
		expr = expr.replace('   ', ' ').replace('  ', ' ').replace('* - ', '* -').replace('+ - ', '+ -')
		expr = expr.replace('/ - ', '/ -').replace('% - ', '% -').replace('^ - ', '^ -').replace('- - ', '- -')

		varies = regex.findall(expr)

		print(varies)

		for var in varies:
			var_str = var_regex.match(var).group(0)
			res = None

			if (var_str not in ALL and not (regex_arg.match(var) and len(regex_arg.match(var)) != len(var))):
				print('Warning: Undefined variable \'', var_str, '\'. Ignored!', sep='')
			elif (regex_arg.match(var) and len(regex_arg.match(var).group(0)) != len(var)):
				koff = '-1' if regex_koff.match(var).group(0) == '-' else regex_koff.match(var).group(0)
				expr = expr.replace(var, koff + ' * ( ' + self.x + ' ) ' if (koff != '') else self.x)
			else:
				if (ALL[var_str].isVal()):
					res = ALL[var_str].resolve()
					koff = '-1' if regex_koff.match(var).group(0) == '-' else regex_koff.match(var).group(0)
					expr = expr.replace(var, koff + ' * ( ' + str(res) + ' ) ' if (koff != '') else str(res))
				else:
					print('Error: Can\'t include variable', var_str)

		return expr

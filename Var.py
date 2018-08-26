import parser
import re

class Var:

	def __init__(self):
		self.val = None
		self.polish = None
		self.type = -1
		self.x = None

	def createFunc(eq, arg, ALL):
		self.type = 1
		self.x = arg

		self.val = self.transform(eq, ALL, arg)
		self.polish = parser.infixToPostfix(self.val).split()

	def createVal(eq, ALL):
		self.type = 0

		self.polish = parser.infixToPostfix(self.transform(eq, ALL))
		self.val = parser.resolveInfix(self.polish)

	def isVal():
		return self.type == 0

	def isFunc():
		return self.type == 1

	def isMatrix():
		return self.type == 2

	def isScalar():
		return self.type == 3

	@staticmethod
	def transform(expr, ALL, arg=''):
		regex = re.compile('(\-?\d*(\.\d+)?)?\w+(\(...\))?')
		var_regex = re.compile('\w+')
		expr = expr.replace(' ', '')
		expr = expr.replace('(', ' ( ').replace(')', ' ) ').replace('^', ' ^ ')
		expr = expr.replace('/', ' / ').replace('*', ' * ').replace('+', ' + ').replace('%', ' % ').replace('-', ' - ')
		expr = expr.replace('   ', ' ').replace('  ', ' ').replace('* - ', '* -').replace('+ - ', '+ -')
		expr = expr.replace('/ - ', '/ -').replace('% - ', '% -').replace('^ - ', '^ -').replace('- - ', '- -')

		varies = regex.findall(expr)

		for var in varies:
			var_str = var_regex.match(var).group(0)

			if (var_str not in ALL and var_str != arg):
				print('Warning: Undefined variable \'', var_str, '\'. Ignored!', sep='')
			elif (var_regex.match(var).group(0) != arg):
				print('Var:' ALL[var_str])

		return expr

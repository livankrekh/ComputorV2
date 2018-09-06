from compv1.polynom_parser import eq_parser, solve

import re
import Var
import parser

def lets_go(arg, VARS):
	new_var = Var.Var()

	if (arg.count('=') > 1):
		raise Exception('Error: equition should have less than 2 \'=\' sign!')

	if (arg.find('?') != -1):
		new_var1 = Var.Var()
		new_var2 = Var.Var()
		arg = arg.replace('?', '')
		arg = arg.split('=')
		func_str = ''

		new_var1.createVal(arg[0], VARS)
		new_var2.createVal(arg[1] if (len(arg) > 1) else "", VARS)

		if ((len(arg) < 2 or new_var2.val == None) and not new_var1.isFunc()):
			new_var1.show()
			return
		func_str = str(new_var1.val) + " = " + (str(new_var2.val) if (new_var2.val != None) else "0")
		if (new_var2.isFunc()):
			func_str = func_str.replace(new_var2.x, new_var1.x)
		func_str = func_str.replace('( ' + str(new_var1.x) + ' )', str(new_var1.x))

		print('\033[1m\033[32m' + func_str + '\033[0m')

		matrix = eq_parser(func_str, 'x' if (new_var1.x == None) else new_var1.x)
		solve(matrix, str(new_var1.x))

	elif (arg.find('=') != -1 and arg.find('?') == -1):
		regex_func = re.compile('[^\d\W]+\([^\d\W]+\)')
		regex_word = re.compile('[^\d\W]+')
		regex_arg = re.compile('\([^\d\W]+\)')
		name = ''
		x = ''
		copy = arg[:]
		arg = arg.split('=')
		arg[0] = arg[0].replace(' ', '')

		if (regex_func.match(arg[0]) and len(regex_func.match(arg[0]).group(0)) == len(arg[0])):
			name = regex_word.match(arg[0]).group(0)
			x = regex_arg.search(regex_func.match(arg[0]).group(0)).group(0)[1:-1]

			if (name == 'i' or x == 'i'):
				raise Exception('\033[1m\033[31mError: Incorrect variable name!\033[0m')
			new_var.createFunc(arg[1], x, VARS)
			new_var.show()
			VARS[name.lower()] = new_var
		elif (regex_word.match(arg[0]) and len(regex_word.match(arg[0]).group(0)) == len(arg[0])):
			name = regex_word.match(arg[0]).group(0)

			if (name == 'i'):
				raise Exception('\033[1m\033[31mError: Incorrect variable\'s name!\033[0m')
			new_var.createVal(arg[1], VARS)
			if (new_var.isFunc()):
				raise Exception('Error: cannot assign function to variable!')
			new_var.show()
			VARS[name.lower()] = new_var
		else:
			raise Exception('Error: Incorrect variable name!')
	elif (arg.find('=') == -1):
		new_var.createVal(arg, VARS)
		new_var.show()
#!/Users/liabanzh/.brew/bin/python3.7

import sys
import re
import Var
import parser

VARS = {}

def lets_go(arg):
	new_var = Var.Var()

	if (arg.find('=') != -1 and arg.find('?') == -1):
		regex_func = re.compile('[^\d\W]+\([^\d\W]+\)')
		regex_word = re.compile('[^\d\W]+')
		regex_arg = re.compile('\([^\d\W]+\)')
		name = ''
		arg = arg.split('=')
		arg[0] = arg[0].replace(' ', '')

		if (regex_func.match(arg[0]) and len(regex_func.match(arg[0]).group(0)) == len(arg[0])):
			name = regex_word.match(arg[0]).group(0)
			x = regex_arg.search(regex_func.match(arg[0]).group(0)).group(0).replace('(', '').replace(')', '')

			new_var.createFunc(arg[1], x, VARS)
			VARS[name] = new_var
			new_var.show()
		elif (regex_word.match(arg[0]) and len(regex_word.match(arg[0]).group(0)) == len(arg[0])):
			name = regex_word.match(arg[0]).group(0)

			new_var.createVal(arg[1], VARS)
			VARS[name] = new_var
			new_var.show()
		else:
			print('Error: Incorrect variable\'s name!')
	elif (arg.find('=') == -1):
		new_var.createVal(arg, VARS)
		new_var.show()

if __name__ == "__main__":
	end = False
	arg = str()

	while not end:
		print('>> ', end='')
		try:
			arg = input()
		except BaseException:
			print('\nBye, bye!')
			exit()

		if (arg.startswith('end')):
			end = True
			break

		lets_go(arg)

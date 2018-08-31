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
		x = ''
		arg = arg.split('=')
		arg[0] = arg[0].replace(' ', '')

		if (regex_func.match(arg[0]) and len(regex_func.match(arg[0]).group(0)) == len(arg[0])):
			name = regex_word.match(arg[0]).group(0)
			x = regex_arg.search(regex_func.match(arg[0]).group(0)).group(0)[1:-1]

			try:
				if (name == 'i' or x == 'i'):
					raise Exception('\033[1m\033[31mError: Incorrect variable name!\033[0m')
				new_var.createFunc(arg[1], x, VARS)
				new_var.show()
				VARS[name.lower()] = new_var
			except Exception as err:
				print('\033[1m\033[31m', err, '\033[0m', sep='')
		elif (regex_word.match(arg[0]) and len(regex_word.match(arg[0]).group(0)) == len(arg[0])):
			name = regex_word.match(arg[0]).group(0)

			try:
				if (name == 'i'):
					raise Exception('\033[1m\033[31mError: Incorrect variable\'s name!\033[0m')
				new_var.createVal(arg[1], VARS)
				new_var.show()
				VARS[name.lower()] = new_var
			except Exception as err:
				print('\033[1m\033[31m', err, '\033[0m', sep='')
		else:
			print('\033[1m\033[31mError: Incorrect variable name!\033[0m')
	elif (arg.find('=') == -1):
		try:
			new_var.createVal(arg, VARS)
			new_var.show()
		except Exception as err:
			print('\033[1m\033[31m', err, '\033[0m', sep='')

if __name__ == "__main__":
	end = False
	arg = str()

	while not end:
		print('>> ', end='')
		try:
			arg = input()
		except BaseException:
			print('\n\033[32mBye, bye!\033[0m')
			exit()

		if (arg.startswith('end') or arg.startswith('exit')):
			end = True
			break

		lets_go(arg)

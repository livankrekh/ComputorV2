#!/Users/liabanzh/.brew/bin/python3.7

import sys
import re
import Var
import parser

VARS = {}

if __name__ == "__main__":
	end = False
	arg = str()

	while not end:
		expr = re.compile('\-?\d+')
		print('> ', end='')
		try:
			arg = input()
		except BaseException:
			print('\nBye, bye!')
			exit()

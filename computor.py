#!./venv/bin/python3

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

import sys
import var_factory
import readline

VARS = {}

if __name__ == "__main__":
	end = False
	arg = str()

	readline.parse_and_bind('"\\C-p": previous-history')
	readline.parse_and_bind('"\\C-n": next-history')

	while not end:
		try:
			arg = input(">> ")
		except BaseException:
			print('\n\033[32mBye, bye!\033[0m')
			exit()

		if (arg == 'exit()'):
			end = True
			break

		try:
			var_factory.lets_go(arg.lower(), VARS)
		except Exception as err:
			print('\033[1m\033[31m', err, '\033[0m', sep='')

#!./venv/bin/python3

try:
	from src.var_factory import lets_go

	import sys
	import readline

except Exception as err:
	print('\033[1m\033[31m', err, '\033[0m', sep='')
	print('\033[1m\033[31mYou need install requirements.txt with pip3 in your virualenv!\033[0m')
	print('\033[1m(venv) > pip3 install -r requirements.txt\033[0m')
	print('\033[1m(venv) > python3 computor.py\033[0m')
	exit()

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
			lets_go(arg.lower(), VARS)
		except Exception as err:
			print('\033[1m\033[31m', err, '\033[0m', sep='')

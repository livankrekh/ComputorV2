#!/Users/liabanzh/.brew/bin/python3.7

import sys
import re
import polynoms

if __name__ == "__main__":
	matrix = []

	for arg in sys.stdin:
		matrix = polynoms.parser(arg)
		print(matrix)

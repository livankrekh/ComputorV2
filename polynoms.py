import re

def toMatrix(polynom):
	matrix = [0, 0, 0]
	power = -1

	for i, elem in enumerate(polynom):
		regexObj = re.match('((\-?\d*(\.\d+)?(\^\d+)?\*?)*\-?\d*(x|X)|(\-?\d+(\.\d+)?(\^\d+)?(\/?\-?\d+)?\*)*\-?\d+)\^?\d*', elem)
		if (regexObj and len(regexObj.group(0)) == len(elem)):
			power = get_polynom_power(elem)
			if (power + 1 > len(matrix)):
				matrix += [0] * (power + 1 - len(matrix))
			matrix[power] += parse_int(elem)
		else:
			print('\033[1m\033[31mWarning! Incorrect polynom member (ignored): \'', elem, '\'\033[0m', sep='')

	return matrix

def parser(polynom_str):
	matrix = []
	matrix2 = []
	polynom1 = []
	polynom2 = []

	if (polynom_str.find('(') != -1 or polynom_str.find(')') != -1):
		print('\033[1m\033[31mError: no bracket handling\033[0m')
		exit()

	polynom_str = polynom_str.split('=')
	polynom1 = list(filter(None, polynom_str[0].split(' ')))
	if (len(polynom_str) > 1):
		polynom2 = list(filter(None, polynom_str[1].split(' ')))
	else:
		print('\033[1m\033[31mWarning: no equal sign (ignored). Value by default: = 0\033[0m')

	polynom1 = transform(polynom1)
	polynom2 = transform(polynom2)

	matrix = toMatrix(polynom1)
	matrix2 = toMatrix(polynom2)

	if (matrix == None or matrix2 == None):
		return None

	if (len(matrix2) > len(matrix)):
		matrix += [0] * (len(matrix2) - len(matrix))

	for i, elem in enumerate(matrix2):
		matrix[i] -= matrix2[i]

	return matrix

def descr(matrix):
	return (matrix[1] * matrix[1]) - (4 * matrix[2] * matrix[0])

def get_number_power(string):
	n = str()
	regex = re.match('\-?\d+(\.\d+)?', string)

	if (regex):
		if (string.find('^') != -1):
			n = string[string.find('^') + 1:]
		else:
			return 1 * float(regex.group(0))

		try:
			return power(float(regex.group(0)), int(n))
		except ValueError:
			return 1
	else:
		return 1

def get_polynom_power(string):
	n = str()

	if (string.find('x^') != -1 or string.find('X^') != -1):
		if (string.find('^') != -1):
			n = string[string.find('^') + 1:]
		else:
			return 1

		try:
			return int(n)
		except ValueError:
			return 1
	elif (string.find('x') != -1 or string.find('X') != -1):
		return 1
	else:
		return 0
			

def power(n, power):
	res = float(1)

	if (power == 0):
		return 1

	if (power > 0):
		for i in range(power):
			res *= n
	else:
		for i in range(power * -1):
			res /= n

	return res


def parse_int(string):
	expr_arr = []
	res = 0

	try:
		return float(string)
	except ValueError:
		regex = re.match('\-?(x|X)\^?\d?', string)
		if (regex and len(regex.group(0)) == len(string)):
			if (string[0] == '-'):
				return -1
			else:
				return 1
		if (string.find('*') != -1):
			res = 1
			expr_arr = string.split('*')

			for expr in expr_arr:
				regex_number = re.match('\-?\d+(\.\d+)?\^?\d*', expr)
				regex_x = re.match('\-?(x|X)\^?\d?', expr)
				regex_d = re.match('\-?\d+\/\-?\d+', expr)

				if (regex_d):
					d_arr = expr.split('/')
					res *= get_number_power(d_arr[0]) / get_number_power(d_arr[1])
				elif (regex_x):
					if (expr[0] == '-'):
						res *= -1
				elif (regex_number):
					res *= get_number_power(regex_number.group(0))

			return res
		elif (string.find('/') != -1):
			d_arr = string.split('/')
			return get_number_power(d_arr[0]) / get_number_power(d_arr[1])
		else:
			regex_new = re.match('\-?\d+\^?\d*', string)

			if (regex_new):
				return get_number_power(regex_new.group(0))
			else:
				return 0

def isSign(string):
	regex = re.match('(\-|\+|\*|\/|\^)+', string)

	if (regex and len(regex.group(0)) == len(string)):
		return True
	return False

def transform(arr):
	new_arr = []

	for i, elem in enumerate(arr):
		if (elem == '-' and i < len(arr) - 1):
			if (len(arr[i + 1]) > 0 and arr[i + 1][0] == '-'):
				arr[i + 1] = arr[i + 1][1:]
			else:
				arr[i + 1] = "-" + arr[i + 1]
		elif ((elem == '*' or elem == '/' or elem == '^') and i > 0 and i < len(arr) - 1):
			arr[i + 1] = arr[i - 1] + arr[i] + arr[i + 1]
			arr[i - 1] = ''

	for i, elem in enumerate(arr):
		if (elem != '' and not isSign(elem)):
			new_arr.append(elem);

	return (new_arr)

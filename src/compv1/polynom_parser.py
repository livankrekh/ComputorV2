#!/Users/liabanzh/.brew/bin/python3.7

from src.compv1.tools import *
import sys
import re

def toMatrix(polynom, x):
	matrix = [0, 0, 0]
	power = -1

	for i, elem in enumerate(polynom):
		regexObj = re.match('((\-?\d*(\.\d+)?(\^\d+)?[\*\/]?)*\-?\d*(' + re.escape(x.lower()) + '|' + re.escape(x.upper()) + ')?|(\-?\d+(\.\d+)?(\^\d+)?(\/?\-?\d+)?\*)*\-?\d+)\^?\d*', elem)
		if (regexObj and len(regexObj.group(0)) == len(elem)):
			power = get_polynom_power(elem, x)
			if (power > 2 or power < 0):
				if (power < 0):
					raise Exception("Error: Polynom degree negative")
				matrix += (power + 1 - len(matrix)) * [0]
			matrix[power] += parse_int(elem, x)
		else:
			print('\033[1m\033[31mWarning! Incorrect polynom member (ignored): \'', elem, '\'\033[0m', sep='')

	return matrix

def eq_parser(polynom_str, x):
	matrix = []
	matrix2 = []
	polynom1 = []
	polynom2 = []

	if (polynom_str.find('(') != -1 or polynom_str.find(')') != -1):
		raise Exception('Error: no bracket handling!')

	polynom_str = polynom_str.split('=')
	polynom1 = list(filter(None, polynom_str[0].split(' ')))

	if (len(polynom_str) > 1):
		polynom2 = list(filter(None, polynom_str[1].split(' ')))

	polynom1 = transform(polynom1, x)
	polynom2 = transform(polynom2, x)

	matrix = toMatrix(polynom1, x)
	matrix2 = toMatrix(polynom2, x)

	if (matrix == None or matrix2 == None):
		return None

	matrix[0] -= matrix2[0]
	matrix[1] -= matrix2[1]
	matrix[2] -= matrix2[2]

	print("\033[1m\033[32mPolynomial degree is:", str(len(matrix) - 1 if (len(matrix) > 3) else degree(matrix)), "\033[0m")

	return matrix

def descriminant(matrix):
	return matrix[1] ** 2 - (4 * matrix[2] * matrix[0])

def solve(matrix, x):
	
	if (matrix[2] != 0):
		if (descriminant(matrix) < 0):
			print('D < 0')

			print('\033[1m\033[32mThe solution is:', x, "=", "(", matrix[1] * -1, "+/-", "\u221A" + str(descriminant(matrix)), ") /", matrix[2] * 2, '\033[0m')
		elif (descriminant(matrix) == 0):
			print('\033[1m\033[32mThe solution is:', x, '=', str((matrix[1] * -1) / (matrix[2] * 2)), "\033[0m")
		else:
			print('\033[1m\033[32mThe solution is: ' + x + "1 = " , str( ((matrix[1] * -1) - descriminant(matrix) ** 0.5) / (matrix[2] * 2) )
												, ", " + x + "2 = ", str( ((matrix[1] * -1) + descriminant(matrix) ** 0.5) / (matrix[2] * 2) )
												, '\033[0m')
	elif (matrix[1] != 0):
		print('\033[1m\033[32mThe solution is:', x, "=", str((matrix[0] * -1) / matrix[1]), "\033[0m")
	else:
		if (matrix[0] == 0):
			print("\033[1m\033[32mThe solution is: every real number\033[0m")
		else:
			print("\033[1m\033[32mThe solution is: no one\033[0m")

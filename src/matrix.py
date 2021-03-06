import src.Var
import re

def lenMatrix(elem):
	n = len(elem)
	m = len(elem[0]) if (n > 0) else 0

	if (type(elem[0]) is not list):
		return [1, n]

	for vector in elem:
		if (len(vector) != m):
			raise Exception("Error: matrix haven't rectangle form")
			return [0, 0]

	return [n, m]

def addMatrix(elem1, elem2):
	matrix = elem1 if (type(elem1) is list) else elem2
	other = elem2 if (matrix == elem1) else elem1

	if (type(other) is float or type(other) is int or type(other) is complex):
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				matrix[i][j] += other

	if (type(other) is list):
		m_len = lenMatrix(matrix)
		o_len = lenMatrix(other)

		if (m_len[0] == o_len[0] and m_len[1] == o_len[1]):
			for i in range(m_len[0] + 1):
				for j in range(m_len[1] + 1):
					matrix[i][j] += other[i][j]
		else:
			raise Exception('Error: Can\'t do addition of matrices with different sizes')

	return matrix

def subMatrix(elem1, elem2):
	matrix = elem1 if (type(elem1) is list) else elem2
	other = elem2 if (matrix == elem1) else elem1

	if (type(other) is float or type(other) is int or type(other) is complex):
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				matrix[i][j] -= other

	if (type(other) is list):
		m_len = lenMatrix(matrix)
		o_len = lenMatrix(other)

		if (m_len[0] == o_len[0] and m_len[1] == o_len[1]):
			for i in range(m_len[0] + 1):
				for j in range(m_len[1] + 1):
					matrix[i][j] -= other[i][j]
		else:
			raise Exception('Error: Can\'t do subtraction of matrices with different sizes')

	return matrix

def multMatrix(elem1, elem2):
	matrix = elem1 if (type(elem1) is list) else elem2
	other = elem2 if (matrix == elem1) else elem1
	res = []

	if (type(other) is float or type(other) is int or type(other) is complex):
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				matrix[i][j] *= other
		return matrix
	elif (type(other) is list):
		m_len = lenMatrix(matrix)
		o_len = lenMatrix(other)

		if (m_len[1] == o_len[0]):
			for i in range(m_len[0]):
				i_res = []
				for j in range(o_len[1]):
					tmp = 0

					for k in range(m_len[1]):
						tmp += matrix[i][k] * other[k][j]

					i_res.append(tmp)
				res.append(i_res)
		else:
			raise Exception('Error: Can\'t do multiplying of matrices with different sizes')

	return res

def parseMatrix(elem, ALL):
	regex_d = re.compile('\-?\d+\.?\d*')
	regex_m = re.compile('\[.*\]')
	elem = elem.replace(' ', '')[1:-1]
	elem = elem.split(';')
	elem = list(filter(None, elem))
	res = []

	for s in elem:
		include = []
		if (regex_m.match(s)):
			s = regex_m.match(s).group(0)[1:-1]

		s = s.split(',')
		s = list(filter(None, s))

		for n in s:
			if (regex_d.match(n) and len(regex_d.match(n).group(0)) == len(n)):
				include.append(float(regex_d.match(n).group(0)))
			else:
				new_var = src.Var.Var()
				new_var.createVal(n, ALL)
				if (new_var.isFunc()):
					raise Exception('Error: can\'t include function in a matrix or vector')
				include.append(new_var.resolve())
		res.append(include)

	lenMatrix(res)

	return res

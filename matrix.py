import re

def addMatrix(elem1, elem2):
	matrix = elem1 if (type(elem1) is list) else elem2
	other = elem2 if (matrix == elem1) else elem1

	if (type(other) is (float or int)):
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				matrix[i][j] += other

def parseMatrix(elem):
    regex_d = re.compile('\-?\d+\.?\d*')
    regex_m = re.compile('\[.*\]')
    elem = elem.replace(' ', '')[1:-1]
    elem = elem.split(';')
    res = []

    for s in elem:
        include = []
        if (regex_m.match(s)):
        	s = regex_m.match(s).group(0)[1:-1]
        
        s = s.split(',')

        for n in s:
            if (regex_d.match(n)):
                include.append(float(regex_d.match(n).group(0)))
            else:
                print('Warning: unknown number \'', n, '\', ignored!')
                include.append(0)
        res.append(include)

    return res
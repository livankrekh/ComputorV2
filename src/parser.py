from src.matrix import *
import re

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[0]

    def size(self):
        return len(self.items)

def cleanFound(arr):
    for i, elem in enumerate(arr):
        if (elem[1] == '' and elem[2] == '' and elem[3] == ''):
            if (elem[5] != ''):
                print('\033[1mWarning: redundant operator \'', elem[5], '\'. Ignored!\033[0m', sep='')
            if (elem[0] == '' and elem[4] == ''):
                arr[i] = None

    arr = list(filter(None, arr))

    return arr

def toNormalForm(expr):
    res = str()
    tmp = expr.replace(' ', '')
    regex = re.compile('(\()?(\-?\d+\.?\d*)?(\-?[^\d\W]+|\[\[.*?\]\;?\])?(\([^\(\)]*\))?(\))?(\-|\+|\*\*?|\/|\%|\^)?')

    tmp = cleanFound(regex.findall(tmp))

    for i, elem in enumerate(tmp):
        if (elem[0] != ''):
            res += ' ( '
        if (elem[1] != ''):
            res += ' ' + elem[1]
        if (elem[2] != ''):
            res += elem[2]
        if (elem[3] != ''):
            res += elem[3]
        if (elem[4] != ''):
            res += ' ' + elem[4] + ' '
        if (elem[5] != ' ' and i < len(tmp) - 1):
            if (tmp[i + 1][1] != '' or tmp[i + 1][2] != ''):
                res += ' ' + elem[5] + ' '

    res = res.replace('  ', ' ')

    return res

def infixToPostfix(infixexpr):
    regex = re.compile('\-?(\d+(\.\d+)?)?[^\d\W]+|\-?\d+(\.\d+)?')
    regex_m = re.compile('\[\[.*?\]\;?\]')
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["**"] = 3
    prec["/"] = 3
    prec["%"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if regex.match(token) or regex_m.match(token):
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

def matrixToStr(matrix):
    res = "["

    for i, elem in enumerate(matrix):
        res += "["

        for j, val in enumerate(elem):
            if (type(val) is complex):
                res += (str(val.real) if (val.real != 0) else "") \
                    + ("+" if (val.real != 0 and val.imag != 0) else "") \
                    + (str(val.imag) + 'i' if (val.imag != 0) else "")
            else:
                res += str(val)
            if (j < len(elem) - 1):
                res += ','
        res += '];'
    
    res += "]"

    return res

def resolveInfix(exprArr, ALL={}):
    regexI = re.compile('\-?\d*\.?\d*(i)')
    regexM = re.compile('\[\[.*?\]\;?\]')
    regex = re.compile('\-?\d+(\.\d+)?')
    stack = []

    if (exprArr == None or exprArr == []):
        return None

    for elem in exprArr:
        try:
            if (len(stack) >= 2 and (type(stack[-2]) is list or type(stack[-1]) is list) and elem in ['/', '*', '+', '-', '%', '^', '**']):
                if (elem == '*' or elem == '**'):
                    stack[-2] = multMatrix(stack[-2], stack[-1])
                elif (elem == '+'):
                    stack[-2] = addMatrix(stack[-2], stack[-1])
                elif (elem == '-'):
                    stack[-2] = subMatrix(stack[-2], stack[-1])
                else:
                    raise Exception('Error: operator \'' + elem + '\' cannot use with matrices!')
                stack.pop()
            elif (len(stack) >= 2 and elem in ['/', '*', '+', '-', '%', '^', '**']):
                if (elem == '/'):
                    stack[-2] = stack[-2] / stack[-1]
                elif (elem == '*'):
                    stack[-2] = stack[-2] * stack[-1]
                elif (elem == '+'):
                    stack[-2] = stack[-2] + stack[-1]
                elif (elem == '-'):
                    stack[-2] = stack[-2] - stack[-1]
                elif (elem == '%'):
                    stack[-2] = stack[-2] % stack[-1]
                elif (elem == '^'):
                    stack[-2] = stack[-2] ** stack[-1]
                elif (elem == '**'):
                    raise Exception('Error: operator \'**\' cannot use with not matrices!')
                stack.pop()
            else:
                if (regex.match(elem)):
                    if (regexI.match(elem)):
                        stack.append(complex(0, float(regex.match(elem).group(0))))
                    else:
                        stack.append(float(regex.match(elem).group(0)))
                elif (regexI.match(elem)):
                    stack.append(complex(0, float(1)))
                elif (regexM.match(elem)):
                    stack.append(parseMatrix(regexM.match(elem).group(0), ALL))
                else:
                    print('\033[1mWarning! Redundant operator \'', elem, '\'. Ignored!\033[0m', sep='')
        except OverflowError:
            raise Exception('Error: Too large result of operation ' + str(stack[-2]) + ' ' + elem + ' ' + str(stack[-1]))
        except TypeError:
            raise Exception('Error: Can\'t resolve next operation' + str(stack[-2]) + ' ' + elem + ' ' + str(stack[-1]))
        except ZeroDivisionError:
            raise Exception('Error: Division by zero in operation ' + str(stack[-2]) + ' ' + elem + ' ' + str(stack[-1]))
        except Exception as err:
            raise Exception(err)

    return stack[-1] if (len(stack) > 0) else None

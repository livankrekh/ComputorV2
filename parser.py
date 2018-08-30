import re
import matrix

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

def infixToPostfix(infixexpr):
    regex = re.compile('\-?(\d+(\.\d+)?)?[^\d\W]+|\-?\d+(\.\d+)?')
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["%"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if regex.match(token):
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

def resolveInfix(exprArr):
    regexI = re.compile('\-?\d*(\.\d+)?(i|j)')
    regexM = re.compile('\[.*\]')
    regex = re.compile('\-?\d+(\.\d+)?')
    stack = []

    if (exprArr == None or exprArr == []):
        return None

    for elem in exprArr:
        try:
            if (len(stack) >= 2 and (type(stack[-2]) is list or type(stack[-1]) is list)):
                if (elem == '*'):
                    stack[-2] = stack[-2] * stack[-1]
                elif (elem == '+'):
                    stack[-2] = stack[-2] + stack[-1]
                elif (elem == '-'):
                    stack[-2] = stack[-2] - stack[-1]
                stack.pop()
            elif (len(stack) >= 2 and elem in ['/', '*', '+', '-', '%', '^']):
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
                stack.pop()
            else:
                if (regex.match(elem)):
                    if (regexI.match(elem)):
                        stack.append(complex(0, float(regex.match(elem).group(0))))
                    elif (regexM.match(elem)):
                        stack.append(matrix.parseMatrix(elem))
                    else:
                        stack.append(float(regex.match(elem).group(0)))
                else:
                    print('Warning! Undefined variable or operand \'', elem, '\'. Ignored!', sep='')
        except OverflowError:
            print('Error: Too large result of operation ' + str(stack[-2]) + ' ' + elem + ' ' + str(stack[-1]))
        except TypeError:
            print('Error: Can\'t resolve next operation' + str(stack[-2]) + ' ' + elem + ' ' + str(stack[-1]))
        except ZeroDivisionError:
            print('Error: Division by zero in operation ' + str(stack[-2]) + ' ' + elem + ' ' + str(stack[-1]))

    return stack[-1] if (len(stack) > 0) else None

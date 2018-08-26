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

def infixToPostfix(infixexpr):
    regex = re.compile('\-?(\d+(\.\d+)?)?\w+|\-?\d+(\.\d+)?')
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
    regexI = re.compile('\-?\d+(\.\d+)?i?')
    regex = re.compile('\-?\d+(\.\d+)?')
    stack = []

    if (exprArr == None or exprArr == []):
        return None

    for elem in exprArr:
        if (len(stack) > 2 and elem in ['/', '*', '+', '-', '%', '^']):
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
        else:    
            if (regex.match(elem)):
                if (regexI.match(elem)):
                    stack.append(complex(0, float(regex.match(elem).group(0))))
                else:
                    stack.append(float(regex.match(elem).group(0)))
            else:
                print('Warning! Undefined variable or operand \'', elem, '\'. Ignored!', sep='')

    return stack[-1] if (len(stack) > 0) else None

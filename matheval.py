import math

class Expression(object):
    def __init__(self):
        self.bind = 0

    def evaluate(self):
        return 0

class Value(Expression):
    def __init__(self, value):
        self.bind = 4
        self.value = value
        self.argpos = [0]

    def evaluate(self):
        return self.value

class Operation(Expression):
    def __init__(self):
        self.args = list()

class Addition(Operation):
    def __init__(self):
        super(Addition,self).__init__()
        self.bind = 3
        self.argpos = [-1, 1]

    def evaluate(self):
        return self.args[0].evaluate() + self.args[1].evaluate()

class Subtraction(Operation):
    def __init__(self):
        super(Subtraction,self).__init__()
        self.bind = 3
        self.argpos = [-1, 1]

    def evaluate(self):
        return self.args[0].evaluate() - self.args[1].evaluate()

class Multiplication(Operation):
    def __init__(self):
        super(Multiplication,self).__init__()
        self.bind = 2
        self.argpos = [-1, 1]

    def evaluate(self):
        return self.args[0].evaluate() * self.args[1].evaluate()

class Division(Operation):
    def __init__(self):
        super(Division,self).__init__()
        self.bind = 2
        self.argpos = [-1, 1]

    def evaluate(self):
        return self.args[0].evaluate() / self.args[1].evaluate()

class PowerOf(Operation):
    def __init__(self):
        super(PowerOf,self).__init__()
        self.bind = 1
        self.argpos = [-1, 1]

    def evaluate(self):
        return self.args[0].evaluate() ** self.args[1].evaluate()

class SquareRoot(Operation):
    def __init__(self):
        super(SquareRoot,self).__init__()
        self.bind = 1
        self.argpos = [1]

    def evaluate(self):
        return math.sqrt(self.args[0].evaluate())

class Factorial(Operation):
    def __init__(self):
        super(Factorial,self).__init__()
        self.bind = 1
        self.argpos = [-1]

    def evaluate(self):
        res = 1
        curr = self.args[0].evaluate()
        while curr > 1:
            res *= curr
            curr -= 1
        return res

class Scope(Expression):
    def __init__(self):
        self.bind  = 0
        self.list = list()

    def evaluate(self):
        curr_bind = 0
        while len(self.list) > 1 and curr_bind < 4:
            index = 0
            while index < len(self.list):
                exp = self.list[index]
                if exp.bind == curr_bind:
                    
                    for pos in exp.argpos:
                        exp.args.append(self.list[index + pos])

                    popargpos = exp.argpos[:]
                    popargpos.sort(reverse=True)
                    for pos in popargpos:
                        self.list.pop(index + pos)

                    indexdiff = 1
                    for pos in popargpos:
                        if pos < 0:
                            indexdiff += pos

                    index += indexdiff
                else:
                    index += 1
            curr_bind += 1

        if len(self.list) == 0:
            return 0
        else:
            return self.list[0].evaluate()

def parse(expression):
    scope_stack = list()
    scope_stack.append(Scope())

    expression = expression.replace(")(", ")*(")
    expression = expression.replace("sqrt", "s")

    current_number = ""
    for c in expression:
        if c.isdigit() or c == "." or (current_number == "" and  c == "-"):
            current_number += c
        else:
            if not current_number == "":
                scope_stack[-1].list.append(Value(float(current_number)))
                current_number = ""
            if c == "(":
                scope_stack.append(Scope())
            elif c == ")":
                scope = scope_stack.pop()
                scope_stack[-1].list.append(Value(scope.evaluate()))
            elif c == "+":
                scope_stack[-1].list.append(Addition())
            elif c == "-":
                scope_stack[-1].list.append(Subtraction())
            elif c == "*":
                scope_stack[-1].list.append(Multiplication())
            elif c == "/":
                scope_stack[-1].list.append(Division())
            elif c == "^":
                scope_stack[-1].list.append(PowerOf())
            elif c == "s":
                scope_stack[-1].list.append(SquareRoot())
            elif c == "!":
                scope_stack[-1].list.append(Factorial())
            

    if not current_number == "":
        scope_stack[-1].list.append(Value(float(current_number)))
    
    return scope_stack[0].evaluate()

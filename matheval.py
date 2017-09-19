class Expression(object):
    def __init__(self):
        self.bind = 0

    def evaluate(self):
        return 0

class Value(Expression):
    def __init__(self, value):
        self.bind = 4
        self.value = value

    def evaluate(self):
        return self.value

class Operation(Expression):
    def __init__(self, value1=Value(0), value2=Value(0)):
        self.value1 = value1
        self.value2 = value2

class Addition(Operation):
    def __init__(self):
        super(Addition,self).__init__()
        self.bind = 3

    def evaluate(self):
        return self.value1.evaluate() + self.value2.evaluate()

class Subtraction(Operation):
    def __init__(self):
        super(Subtraction,self).__init__()
        self.bind = 3

    def evaluate(self):
        return self.value1.evaluate() - self.value2.evaluate()

class Multiplication(Operation):
    def __init__(self):
        super(Multiplication,self).__init__()
        self.bind = 2

    def evaluate(self):
        return self.value1.evaluate() * self.value2.evaluate()

class Division(Operation):
    def __init__(self):
        super(Division,self).__init__()
        self.bind = 2

    def evaluate(self):
        return self.value1.evaluate() / self.value2.evaluate()

class PowerOf(Operation):
    def __init__(self):
        super(PowerOf,self).__init__()
        self.bind = 1

    def evaluate(self):
        return self.value1.evaluate() ** self.value2.evaluate()

class Scope(Expression):
    def __init__(self):
        self.bind  = 0
        self.list = list()

    def evaluate(self):
        curr_bind = 0
        while len(self.list) > 1 and curr_bind < 5:
            max_len = len(self.list)
            index = 0
            while index < max_len:
                exp = self.list[index]
                if exp.bind == curr_bind:
                    exp.value1 = self.list[index-1]
                    exp.value2 = self.list[index+1]
                    self.list.pop(index+1)
                    self.list.pop(index-1)
                    max_len -= 2
                else: index += 1
            curr_bind += 1

        return self.list[0].evaluate()

def parse(expression):
    scope_stack = list()
    scope_stack.append(Scope())


    current_number = ""
    for c in expression:
        if c.isdigit() or c == ".":
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

    if not current_number == "":
        scope_stack[-1].list.append(Value(float(current_number)))
    
    return scope_stack[0].evaluate()
            
#s = parse("(3+2)^2*4")
#print(s)

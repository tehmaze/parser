import math
import cmath
from parser.base import Parser
from parser.calc.tokens import tokenize

class Calc(Parser):
    def reader(self, program, **scope):
        scope.update({
            'e': math.e, 'pi': math.pi,
        })

        for token, value in self.tokenize(program):
            if token == 'long':
                yield self.symbols['(literal)'](self, long(value))
            elif token == 'float':
                yield self.symbols['(literal)'](self, float(value))
            elif token == 'complex':
                yield self.symbols['(literal)'](self, complex(value))
            elif token == 'operator':
                yield self.symbols[value](self)
            elif token == 'name':
                if value in self.symbols:
                    yield self.symbols[value](self)
                elif value in scope:
                    yield self.symbols['(literal)'](self, scope[value])
                else:
                    raise NameError('Name %r is not defined' % (value,))
            else:
                raise SyntaxError('Unknown symbol %r' % (token,))
        yield self.symbols['(end)'](self)

# Calc object
calc = Calc(tokenize)

# Definition of symbols
calc.infix('<<', 100)
calc.infix('>>', 100)
calc.infix('+', 110)
calc.infix('-', 110)
calc.infix('*', 120)
calc.infix('/', 120)
calc.infix('//', 120)
calc.infix('%', 120)
calc.prefix('-', 130)
calc.prefix('+', 130)
calc.prefix('~', 130)
calc.infixr('**', 140)
calc.symbol('(literal)')
calc.symbol('(end)')
calc.symbol(')')

@calc.method(calc.symbol('('))
def nud(self):
    expr = self.expression()
    self.advance(')')
    return expr

@calc.method(calc.symbol('(literal)'))
def nud(self):
    return self.value

@calc.method(calc.symbol('+'))
def led(self, left):
    return left + self.expression(110)

@calc.method(calc.symbol('-'))
def led(self, left):
    expr = self.expression(110)
    return left - expr

@calc.method(calc.symbol('*'))
def led(self, left):
    return left * self.expression(120)

@calc.method(calc.symbol('%'))
def led(self, left):
    return left % self.expression(120)

@calc.method(calc.symbol('/'))
def led(self, left):
    return left / self.expression(120)

@calc.method(calc.symbol('//'))
def led(self, left):
    return left // self.expression(120)

@calc.method(calc.symbol('**'))
def led(self, left):
    return left ** self.expression(140)

# Basic functions
@calc.method(calc.symbol('log'))
def nud(self):
    return math.log(self.expression())

@calc.method(calc.symbol('cos'))
def nud(self):
    return math.cos(self.expression())

@calc.method(calc.symbol('sin'))
def nud(self):
    return math.sin(self.expression())

@calc.method(calc.symbol('tan'))
def nud(self):
    return math.tan(self.expression())

@calc.method(calc.symbol('sqrt'))
def nud(self):
    return math.sqrt(self.expression())

@calc.method(calc.symbol('pow'))
def nud(self):
    return math.pow(self.expression(), self.expression())

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

@calc.method(calc.symbol('acos'))
def nud(self):
    return math.acos(self.expression())

@calc.method(calc.symbol('acosh'))
def nud(self):
    return math.acosh(self.expression())

@calc.method(calc.symbol('asin'))
def nud(self):
    return math.asin(self.expression())

@calc.method(calc.symbol('asinh'))
def nud(self):
    return math.asinh(self.expression())

@calc.method(calc.symbol('atan'))
def nud(self):
    return math.atan(self.expression())

@calc.method(calc.symbol('atanh'))
def nud(self):
    return math.atanh(self.expression())

@calc.method(calc.symbol('ceil'))
def nud(self):
    return math.ceil(self.expression())

@calc.method(calc.symbol('cos'))
def nud(self):
    return math.cos(self.expression())

@calc.method(calc.symbol('cosh'))
def nud(self):
    return math.cosh(self.expression())

@calc.method(calc.symbol('degrees'))
def nud(self):
    return math.degrees(self.expression())

@calc.method(calc.symbol('erf'))
def nud(self):
    return math.erf(self.expression())

@calc.method(calc.symbol('erfc'))
def nud(self):
    return math.erfc(self.expression())

@calc.method(calc.symbol('exp'))
def nud(self):
    return math.exp(self.expression())

@calc.method(calc.symbol('fabs'))
def nud(self):
    return math.fabs(self.expression())

@calc.method(calc.symbol('factorial'))
def nud(self):
    return math.factorial(self.expression())

@calc.method(calc.symbol('floor'))
def nud(self):
    return math.floor(self.expression())

@calc.method(calc.symbol('fmod'))
def nud(self):
    return math.fmod(self.expression())

@calc.method(calc.symbol('frexp'))
def nud(self):
    return math.frexp(self.expression())

@calc.method(calc.symbol('gamma'))
def nud(self):
    return math.gamma(self.expression())

@calc.method(calc.symbol('hypot'))
def nud(self):
    return math.hypot(*self.expression())

@calc.method(calc.symbol('isinf'))
def nud(self):
    return math.isinf(self.expression())

@calc.method(calc.symbol('isnan'))
def nud(self):
    return math.isnan(self.expression())

@calc.method(calc.symbol('ldexp'))
def nud(self):
    return math.ldexp(*self.expression())

@calc.method(calc.symbol('lgamma'))
def nud(self):
    return math.lgamma(self.expression())

@calc.method(calc.symbol('log'))
def nud(self):
    return math.log(self.expression())

@calc.method(calc.symbol('log10'))
def nud(self):
    return math.log10(self.expression())

@calc.method(calc.symbol('log1p'))
def nud(self):
    return math.log1p(self.expression())

@calc.method(calc.symbol('radians'))
def nud(self):
    return math.radians(self.expression())

@calc.method(calc.symbol('modf'))
def nud(self):
    return math.modf(self.expression())

@calc.method(calc.symbol('pow'))
def nud(self):
    return math.pow(*self.expression())

@calc.method(calc.symbol('sin'))
def nud(self):
    return math.sin(self.expression())

@calc.method(calc.symbol('sinh'))
def nud(self):
    return math.sinh(self.expression())

@calc.method(calc.symbol('tan'))
def nud(self):
    return math.tan(self.expression())

@calc.method(calc.symbol('tanh'))
def nud(self):
    return math.tanh(self.expression())

@calc.method(calc.symbol('trunc'))
def nud(self):
    return math.trunc(self.expression())

@calc.method(calc.symbol('sqrt'))
def nud(self):
    return math.sqrt(self.expression())

@calc.method(calc.symbol('pow'))
def nud(self):
    return math.pow(self.expression(), self.expression())

# aliases
calc.alias('deg', 'degrees')
calc.alias('fac', 'factorial')
calc.alias('rad', 'radians')

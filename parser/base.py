# Crude symbol based top down operator presedence parser, as originally
# implemented by Vaughan Pratt[1] and Douglas Crockford[2].
#
# [1]: http://doi.acm.org/10.1145/512927.512931
# [2]: http://javascript.crockford.com/tdop/tdop.html

import re
#from nagios_cli.filters.tokenizer import tokenize
from symbol import SymbolBase
from tokenizer import tokenize


class Parser(object):
    symbols = {}
    token = None
    next = None
    variables = []

    def __init__(self, tokenize=tokenize):
        self.tokenize = tokenize

    def symbol(self, ident, bp=0):
        '''
        Gets (and create if not exists) as named symbol.

        Optionally, you can specify a binding power (bp) value, which will be used
        to control operator presedence; the higher the value, the tighter a token
        binds to the tokens that follow.
        '''
        try:
            s = self.symbols[ident]
        except KeyError:
            class s(SymbolBase):
                pass
            s.__name__ = 'symbol-%s' % (ident,)
            s.ident = ident
            s.lbp = bp
            self.symbols[ident] = s
        else:
            s.lbp = max(bp, s.lbp)
        return s

    def alias(self, alias, ident):
        self.symbols[alias] = self.symbols[ident]

    # Helper functions

    def infix(self, ident, bp):
        def led(this, left):
            return self.expression(bp)
        self.symbol(ident, bp).led = led

    def infixr(self, ident, bp):
        def led(this, left):
            return self.expression(bp-1)
        self.symbol(ident, bp).led = led

    def prefix(self, ident, bp):
        def nud(this):
            return self.expression(bp)
        self.symbol(ident).nud = nud

    def constant(self, ident, value):
        @self.method(self.symbol(ident))
        def nud(this):
            this.ident = '(literal)'
            return value

    def method(self, symbol):
        '''
        Symbol decorator.
        '''
        assert issubclass(symbol, SymbolBase)
        def wrapped(fn):
            setattr(symbol, fn.__name__, fn)
        return wrapped

    def advance(self, ident=None):
        if ident and self.token.ident != ident:
            raise SyntaxError('Expected %r, got %r' % (ident, self.token.ident))
        self.token = self.next()

    def expression(self, rbp=0):
        t = self.token
        self.token = self.next()
        left = t.nud()
        while rbp < self.token.lbp:
            t = self.token
            self.token = self.next()
            left = t.led(left)
        return left

    def parse(self, program, **scope):
        self.next = self.reader(program, **scope).next
        self.token = self.next()
        return self.expression()

    def reader(self, program, **scope):
        scope.update({
            'None': None, 'null': None, 
            'True': True, 'true': True,
            'False': False, 'false': False,
            'empty': '',
        })
        for kind, value in tokenize(program):
            #print (kind, value),
            if kind == 'literal':
                s = self.symbols['(literal)']()
                try:
                    s.value = scope[value]
                except KeyError:
                    raise NameError('Name %r is not defined' % (value,))
                yield s
            elif kind == 'variable':
                s = self.symbols['(literal)']()
                try:
                    s.value = self.variables[int(value[1:])]
                except IndexError:
                    s.value = None
                yield s
            elif kind == 'string':
                s = self.symbols['(literal)']()
                s.value = value[1:-1]
                yield s
            elif kind == 'number':
                s = self.symbols['(literal)']()
                s.value = long(value)
                yield s
            elif kind == 'float':
                s = self.symbols['(literal)']()
                s.value = float(value)
                yield s
            elif kind == 'symbol':
                yield self.symbols[value]()
            else:
                raise SyntaxError('Unknown operator %s' % (kind,))

        #print '->',
        yield self.symbols['(end)']()

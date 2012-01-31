# Crude symbol based top down operator presedence parser, as originally
# implemented by Vaughan Pratt[1] and Douglas Crockford[2].
#
# [1]: http://doi.acm.org/10.1145/512927.512931
# [2]: http://javascript.crockford.com/tdop/tdop.html

import re

class SymbolBase(object):
    ident = None
    value = None
    first = None

    def __init__(self, parser, value=None):
        self.parser = parser
        self.value = value

        # Alias methods for easy access
        for method in ['advance', 'expression']:
            setattr(self, method, getattr(self.parser, method))

    def nud(self):
        '''
        Null declaration, is used when a token appears at the beginning
        of a language construct.
        '''
        raise SyntaxError('Syntax error %r' % (self.ident,))

    def led(self, left):
        '''
        Left denotation, is used when it appears inside the construct.
        '''
        raise SyntaxError('Unknown operator %r' % (self.ident,))


from parser.tokens import Scanner, group, tokenizer
from parser.tokens import PNT_FLOAT, EXP_FLOAT, IMG_NUMBER, INT_NUMBER, WHITESPACE, NAME

OPERATOR = group(
    r'[-+*%]',
    r'(?:/|//)',
    r'\*\*',
)

GROUP = group(
    r'[\(\)]',
    r'[\[\]]',
)

scanner = Scanner((
    (OPERATOR,          lambda scanner, token: ('operator', token)),
    (GROUP,             lambda scanner, token: ('operator', token)),
    (IMG_NUMBER,        lambda scanner, token: ('complex',  token)),
    (PNT_FLOAT,         lambda scanner, token: ('float',    token)),
    (INT_NUMBER,        lambda scanner, token: ('long',     token)),
    (EXP_FLOAT,         lambda scanner, token: ('expo',     token)),
    (NAME,              lambda scanner, token: ('name',     token)),
    (WHITESPACE,        None),
))

tokenize = tokenizer(scanner)

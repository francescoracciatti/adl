# -----------------------------------------------------------------------------
# lexer.py
#
# Author: Francesco Racciatti (racciatti.francesco@gmail.com)
#
# This module contains the lexer.
# -----------------------------------------------------------------------------

import enum
import lexer.keywords as keywords
import ply.lex as lex


@enum.unique
class BasicSymbol(enum.Enum):
    """
    The types for basic symbols.
    """
    RESERVED = 'reserved'
    OPERATOR = 'operator'
    OPERAND = 'operand'


@enum.unique
class BasicOperandType(enum.Enum):
    """
    The types for basic operand.
    """
    IDENTIFIER = 'identifier'
    INTEGER = 'integer'
    STRING = 'string'
    REAL = 'real'
    
    @classmethod
    def tokens(cls):
        return _tokens(cls)


@enum.unique
class BasicOperatorType(enum.Enum):
    """
    The types for basic operators.
    """
    ADDASSIGN = '+='
    SUBASSIGN = '-='
    MULASSIGN = '*='
    DIVASSIGN = '/='
    MODASSIGN = '%='
    # Comparison operators
    NOTEQUALTO = '!='
    EQUALTO = '=='
    GREQTHN = '>='
    LSEQTHN = '<='
    GRTHN = '>'
    LSTHN = '<'
    # Basic assignment operator
    ASSIGN = '='
    # Basic operators
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    EXP = '**'
    # Logical operators
    LAND = '&&'
    LOR = '||'
    # Punctuation
    LROUND = '('
    RROUND = ')'
    LBRACK = '['
    RBRACK = ']'
    LCURVY = '{'
    RCURVY = '}'
    COMMA = ','

    @classmethod
    def tokens(cls):
        return _tokens(cls)

def _tokens(cls):
    """
    Builds the list of the names of an enum.Enum class.
    """
    tokens = []
    for e in cls:
        tokens.append(e.name)
    return tokens


# Tuple of basic operands
operands = (
    # The base types
    'STRING',
    'REAL',
    'INTEGER',
    # The identifiers
    'IDENTIFIER',
)

# Tuple of basic operators
operators = (
    # Compound assignment operators
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'MODASSIGN',
    # Comparison operators
    'NOTEQUALTO',
    'EQUALTO',
    'GREQTHN',
    'LSEQTHN',
    'GRTHN',
    'LSTHN',
    # Basic assignment operator
    'ASSIGN',
    # Basic operators
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'EXP',
    # Logical operators
    'LAND',
    'LOR',
    # Punctuation
    'LROUND',
    'RROUND',
    'LBRACK',
    'RBRACK',
    'LCURVY',
    'RCURVY',
    'COMMA',
)

# TODO make it a tuple
# The list of the AML tokens
tokens = BasicOperatorType.tokens() + BasicOperandType.tokens() + keywords.tokens()

# TODO remove if it is possible or change name
# The dict of the AML reserved keywords
reserved = keywords.rview()

# Regex rules for compound assignment operators
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_MODASSIGN = r'%='
# Regex rules for comparison operators
t_NOTEQUALTO = r'!='
t_EQUALTO = r'=='
t_GREQTHN = r'>='
t_LSEQTHN = r'<='
t_GRTHN = r'>'
t_LSTHN = r'<'
# Regex rule for basic assignment operator
t_ASSIGN = r'='
# Regex rules for basic operators
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_EXP = r'\*\*'
# Logical operators
t_LAND = r'\&\&'
t_LOR = r'\|\|'
# Regex rules for punctuation
t_LROUND = r'\('
t_RROUND = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCURVY = r'\{'
t_RCURVY = r'\}'
t_COMMA = r'\,'


# Regex rule for strings
def t_STRING(t):
    r'\"([^\\"]|(\\.))*\"'
    t.value = t.value.replace("\"", "")
    return t
    

# Regex rule for signed real numbers
def t_REAL(t):
    r'-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        raise SyntaxError("real number badly defined")
    return t


# Regex rule for signed integer numbers
def t_INTEGER(t):
    r'-?\d+'
    try:
	    t.value = int(t.value)
    except ValueError:
        raise SyntaxError("integer number badly defined")
    return t


# Regex rule for identifiers
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    # Checks if the identifier is a reserved keyword
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


# Regex rule to ignore tab occurrences
t_ignore = " \t"


# Regex rule to ignore comments
def t_comment(t):
    r'\#.*'
    pass


# Regex rule to increment the line counter when new lines occur
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    pass    


# Regex rule for wrong statement or characters
def t_error(t):
    raise SyntaxError("illegal character " + str(t.value[0]))
    # TODO check if the fix does work and remove the old code below
    #print("[Error] illegal character " + str(t.value[0]))
    #t.lexer.skip(1)
	
	
# Builds the lexer
lexer = lex.lex()

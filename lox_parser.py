#
# Lox interperter
# following book: 'Crafting Interpreters'
# Created by fleacat
#
#
#

"""
Grammar: (with C style precedence rules)

expression -> equality
equality -> comparison ( EQUALITY_OP comparison )*
comparison -> addition ( COMPARISON_OP addition )*
addition -> multiplication ( ADDITION_OP multiplication )*
multiplication -> unary ( MULT_OP unary )*
unary -> (UNARY_OP primary) | primary
primary -> NUMBER | STRING | "false" | "true" | "nil" | ( "(" expression ")" )

"""

from lox_token import *
from lox_consumed_list import ConsumedList
from lox_expr import *

class ParseError(Exception):
	pass

EQUALITY_OPS = set( ['==', '!='] )
COMPARISON_OPS = set( ['<', '>', '<=', '>='] )
ADDITION_OPS = set( ['+', '-'] )
MULT_OPS = set( ['*', '/'] )
UNARY_OPS = set( ['-', '!'] )
PRIMARY_TYPES = set( [IDENTIFIER, STRING, NUMERIC, "false", "true", "nil"] )


def build(tokens):
	return equality(tokens)

def equality(tokens):
	expr = comparison(tokens)
	while tokens.peek().isA(EQUALITY_OPS):
		op = tokens.consume()
		right = comparison(tokens)
		expr=EqualityExpr(expr, op, right)
	return expr

def comparison(tokens):
	expr = addition(tokens)
	while tokens.peek().isA(COMPARISON_OPS):
		op = tokens.consume()
		right = addition(tokens)
		expr = ComparisonExpr(expr, op, right)
	return expr

def addition(tokens):
	expr = multiplication(tokens)
	while tokens.peek().isA(ADDITION_OPS):
		op = tokens.consume()
		right = multiplication(tokens)
		expr = AdditionExpr(expr, op, right)
	return expr

def multiplication(tokens):
	expr = unary(tokens)
	while tokens.peek().isA(MULT_OPS):
		op = tokens.consume()
		right = unary(tokens)
		expr = MultiplicationExpr(expr, op, right)
	return expr

def unary(tokens):
	if tokens.peek().isA(UNARY_OPS):
		op = tokens.consume()
		return UnaryExpr(op, unary(tokens))
	else:
		return primary(tokens)


def primary(tokens):
	token = tokens.consume()
	if token.isA(PRIMARY_TYPES):
		return PrimaryExpr(token)
	elif token.isA("("):
		e = build(tokens)
		end_parens = tokens.consume()
		if end_parens.isA(")"):
			return e
		else:
			raise ParseError(
				"No match found for parenthesis at line {0}".format(token.linenum) )
	else:
		raise ParseError(
			"Expected primary token, but got {0} at line {1}".format(token, token.linenum) )




if __name__ == '__main__':
	from lox_scanner import SourceFile, scanAll

	source = SourceFile("-3 * (3 + 1) == (5 - 10 - 7)")
	token_list = scanAll(source)
	print("Scanned tokens:")
	for token in token_list:
		print(token)
	print("")
	#wrap plain list for parser
	token_list = ConsumedList(token_list)

	print("Parsed syntax tree:")
	ast = build(token_list)
	print(ast)
	print("")

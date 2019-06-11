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

class Parser:
	def __init__(self,tokens):
		self.tokens = ConsumedList(tokens)

	def parse(self):
		return self.expr()

	def expr(self):
		return self.equality()

	def equality(self):
		expr = self.comparison()
		while self.tokens.peek().isA(EQUALITY_OPS):
			op = self.tokens.consume()
			right = self.comparison()
			expr=EqualityExpr(expr, op, right)
			return expr

	def comparison(self):
		expr = self.addition()
		while self.tokens.peek().isA(COMPARISON_OPS):
			op = self.tokens.consume()
			right = self.addition()
			expr = ComparisonExpr(expr, op, right)
			return expr

	def addition(self):
		expr = self.multiplication()
		while self.tokens.peek().isA(ADDITION_OPS):
			op = self.tokens.consume()
			right = self.multiplication()
			expr = AdditionExpr(expr, op, right)
			return expr

	def multiplication(self):
		expr = self.unary()
		while self.tokens.peek().isA(MULT_OPS):
			op = self.tokens.consume()
			right = self.unary()
			expr = MultiplicationExpr(expr, op, right)
			return expr

	def unary(self):
		if self.tokens.peek().isA(UNARY_OPS):
			op = self.tokens.consume()
			return UnaryExpr(op, self.unary())
		else:
			return self.primary()


	def primary(self):
		token = self.tokens.consume()
		if token.isA(PRIMARY_TYPES):
			return PrimaryExpr(token)
		elif token.isA("("):
			e = self.expr()
			end_parens = self.tokens.consume()
			if end_parens.isA(")"):
				return e
			else:
				raise ParseError("No match found for parenthesis at line {0}".format(token.linenum) )
		else:
			raise ParseError("Expected primary token, but got {0} at line {1}".format(token, token.linenum) )




if __name__ == '__main__':
	from lox_scanner import SourceFile, scanAll

	source = SourceFile("-3 * (3 + 1) == (5 - 10 - 7)")
	tokens = scanAll(source)
	print("Scanned tokens:")
	for token in tokens:
		print(token)
	print("")

	parser = Parser(tokens)

	ast = parser.parse()

	print("Parsed syntax tree:")
	ast = build(token_list)
	print(ast)
	print("")

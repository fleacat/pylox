#
# Lox interperter
# following book: 'Crafting Interpreters'
# Created by fleacat
#
#
#

#Token Types
#most types match the string that makes them up
#others are special ALL CAPS

SINGLE_CHAR_TYPES = set([
	'(', ')', '{', '}', ',', '.', '-', '+', ';', '/', '*', '!', '=', '>', '<' ])

DOUBLE_CHAR_TYPES = set([
	'!=', '==', '>=', '<=' ])

KEYWORDS = set([
	'and', 'class', 'else', 'false', 'for', 'fun', 'if', 'nil', 'or',
	'print', 'return', 'super', 'this', 'true', 'var', 'while' ])

IDENTIFIER = "INDENTIFIER"
STRING = "STRING"
NUMERIC = "NUMERIC"
EOF = "EOF"

class Token:
	def __init__(self, token_type, linenum, contents=None):
		self.token_type = token_type
		self.contents = contents
		self.linenum = linenum

	def __str__(self):
		if self.contents is None:
			return "Token({0})[{1}]".format(self.token_type, self.linenum)
		else:
			return "Token({0}, '{1}')[{2}]".format(self.token_type, self.contents, self.linenum)

	def isA(self, token_type):
		if hasattr(token_type, '__iter__'):
			return self.token_type in token_type
		else:
			return self.token_type == token_type

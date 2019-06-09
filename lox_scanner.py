#
# Lox interperter
# following book: 'Crafting Iterpreters'
# Created by fleacat
#

import re
from lox_token import *
from lox_consumed_list import ConsumedList

alpha_re = re.compile(r'^[a-zA-Z_]+$')
def isAlpha(inp):
	return (inp != None) and alpha_re.match(inp) != None

alphanum_re = re.compile(r'^\w+$')
def isAlphaNumeric(inp):
	return (inp != None) and alphanum_re.match(inp) != None

ws_re = re.compile(r'^\s+$')
def isWhiteSpace(inp):
	return (inp != None) and ws_re.match(inp) != None

number_re = re.compile(r'^\d+$')
def isNumber(inp):
	return (inp != None) and number_re.match(inp) != None


class SourceFile(ConsumedList):
	def __init__(self, contents):
		ConsumedList.__init__(self, contents)
		self.line = 1

	def consume(self):
		ch = ConsumedList.consume(self)
		if ch == '\n':
			self.line += 1
		return ch

	def getLine(self):
		return self.line

	def reset(self):
		ConsumedList.reset()
		self.line = 1

class ScanError(Exception):
	pass

#consumes 1 or more source characters and returns the next token
def scan(source):
	while True:
		ch = source.consume()
		if not isWhiteSpace(ch):
			break
	linenum = source.getLine()
	if ch is None:
		return Token(EOF, linenum)

	if ch == '\"':
		#start of string
		contents = ""
		ch = source.consume()
		while ch != '\"':
			if ch is None:
				raise ScanError("Unmatched quotes for string at line {0}".format(start_line))
			else:
				contents += ch
			ch = source.consume()
		return Token(STRING, linenum, contents)
	if isNumber(ch):
		contents = ch
		next_ch = source.peek()
		while isNumber(next_ch) or next_ch == '.':
			contents += source.consume()
			next_ch = source.peek()
		return Token(NUMERIC, linenum, float(contents))
	if isAlpha(ch):
		#identifier or keyword
		contents = ch
		while isAlphaNumeric(source.peek()):
			contents += source.consume()
		if contents in KEYWORDS:
			return Token(contents, linenum); #return as a keyword
		else:
			return Token(IDENTIFIER, linenum, contents)
	#check for other tokens
	if source.peek() != None:
		two_ch = ch + source.peek()
		if two_ch in DOUBLE_CHAR_TYPES:
			source.consume()
			return Token(two_ch, linenum)
	if ch in SINGLE_CHAR_TYPES:
		return Token(ch, linenum)
	#didn't match anything
	raise ScanError("Could not tokenize '{0}' at line {1}".format(ch, linenum))

def scanAll(source):
	token_list = []
	while True:
		token = scan(source)
		token_list.append(token)
		if token.token_type == EOF:
			return token_list


if __name__ == '__main__':
	#test SourceFile and scanner

	source_text = "x = 1 + 2;\nx = 3 * x;\nprint x;\n"
	source = SourceFile(source_text)
	while source.peek() != None:
		line = source.getLine()
		print("Found {0} at line {1}".format(source.consume(), line))


	print("isAlpha('c') is {0}".format(isAlpha('c')))
	print("isAlpha('c4') is {0}".format(isAlpha('c4')))
	print
	print("Tokenizing test:")
	source_text = "x = \"blah\";\nx_3 = x + \" grr\";\nprint x_3;\n"
	source_text += "y = 7.4;\nprint y;\n"
	source = SourceFile(source_text)
	tokens = scanAll(source)
	for t in tokens:
		print(t)

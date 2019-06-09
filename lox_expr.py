#
# Lox interperter
# following book: 'Crafting Interpreters'
# Created by pjht
#
#
#

class BinaryExpr:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def __str__(self):
		return "(" + self.op.token_type + " " + str(self.left) + " " + str(self.right) + ")"

class EqualityExpr(BinaryExpr):
	pass

class ComparisonExpr(BinaryExpr):
	pass

class MultiplicationExpr(BinaryExpr):
	pass

class AdditionExpr(BinaryExpr):
	pass

class UnaryExpr:
	def __init__(self, operator, operand):
		self.operator = operator
		self.operand = operand

	def __str__(self):
		return "(" + self.operator.token_type + " " + str(self.operand) + ")"

class PrimaryExpr:
	def __init__(self, token):
		self.token = token

	def getValue(self):
		if self.token.contents is not None:
			return self.token.contents
		if self.token.isA("true"):
			return True
		if self.token.isA("false"):
			return False
		if self.token.isA("nil"):
			return None
	def __str__(self):
		return str(self.getValue())

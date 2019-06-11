#
# Lox interperter
# following book: 'Crafting Interpreters'
# Created by pjht
#
#
#

from lox_expr import *

def isTruthy(value):
  if value == None:
    return False
  if value == True or value == False:
    return value
  return True

class Interpreter:

  def __init__(self, ast):
    self.ast = ast

  def interpret(self):
    self.__interpret(self.ast)

  def __interpret(self, expr):
    method = getattr(self, "interpret_"+expr.__class__.__name__)
    method(expr)

  def interpret_PrimaryExpr(self, expr):
    return expr.getValue()

  def interpret_UnaryExpr(self, expr):
    operand = self.__interpret(expr.operand);

    if expr.operator.token_type == '!':
      return !isTruthy(right)

    if expr.operator.token_type == '-':
      return -right

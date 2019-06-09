#
# Lox interperter
# following book: 'Crafting Interpreters'
# Created by fleacat
#
#
#

#wraps around list or array to provide, consumed token interface
#used by scanner and parser
class ConsumedList:
	def __init__(self, contents):
		self.contents = contents
		self.position = 0

	def _get_element(self, pos):
		#returns None if at end
		if pos >= len(self.contents):
			return None
		else:
			return self.contents[pos]

	def consume(self):
		e = self._get_element(self.position)
		self.position += 1
		return e

	def peek(self):
		return self._get_element(self.position)

	def peekNext(self):
		return self._get_element(self.position+1)

	def reset(self):
		self.position = 0

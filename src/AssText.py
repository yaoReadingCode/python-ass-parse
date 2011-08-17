#!/usr/bin/env python
# coding: utf-8

class AssText:
	"""
	"""
	def __init__(self, text = ''):
		if not text:
			self.text = ''
		else:
			self.text = text
	
	def parse(self, text):
		"""
		parse ass tag
		"""
		self.text = text
		pass
		
def _test_AssText():
	"""
	test case
	"""
	print 'AssText Test:'

if __name__ == "__main__":
	_test_AssText()

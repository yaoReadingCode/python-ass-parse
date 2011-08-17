#!/usr/bin/env python
# coding: utf-8
"""
    Python Ass Parser
"""

from AssFile import *
from AssScriptInfo import *
from AssStyle import *
from AssEvent import *

##class AssParseBase:
##	"""
##	ASS解析基类
##	实现基本的通用功能
##	"""
##	def __init__(self):
##		print ('AssParseBase init')
	
class AssParse(AssFile):
	"""
	Ass Pase Class
	"""
	def __init__(self, filename, encoding = 'utf-8', err_ignore = False):
		"""
		初始化here
		"""
		AssFile.__init__(self, filename, encoding)
		self.script_info = AssScriptInfo()
		self.styles = AssStyles()
		self.events = AssEvents()
		self.section = ''
		self.version = 0		#self.version     0: v4 style;  1: v4+ style;  2: v4++ style
		self.parse()
	
	def parse(self):
		"""
		解析
		"""
		for i in range(len(self.lines)):
			self.parse_line(self.lines[i])
		
	def parse_line(self, line):
		try:
			if line.lower() == '[script info]':
				self.section = '[Script Info]'
				
			elif line.lower() == '[v4 styles]':
				self.section = '[V4+ Styles]'
				self.version = 0
				
			elif line.lower() == '[v4+ styles]':
				self.section = '[V4+ Styles]'
				self.version = 1
				
			elif line.lower() == '[v4++ styles]':
				self.section = '[V4+ Styles]'
				self.version = 2
				
			elif line.lower() == '[events]':
				self.section = '[Events]'
				
			elif not self.section:
				raise UnknowDataError('Unknow Section: <%s>' % (line))
			
			else:
				if self.section == '[Script Info]':
					self.script_info.parse(line)#line, self.version)
				elif self.section == '[V4+ Styles]':
					self.styles.parse(line, self.version)
				elif self.section == '[Events]':
					self.events.parse(line, self.version)
				else:
					raise UnknowDataError("Unkonw Data: <%s>" % (line))

		except UnknowDataError, err_msg:
			print UnknowDataError, ':', err_msg

if __name__ == "__main__" :
	# just for test

	filename1 = './l.ass'
	filename2 = './l.ssa'
	coding = 'utf-8'
	#import sys
	#f = open('./l.txt', 'w')
	#sys.stdout = f

	obj1 = AssParse(filename1, coding)
	#obj1.file_dump()
	obj1.script_info.dump()
	obj1.styles.dump()
	obj1.events.dump()
	#obj1.parse()
	#obj1.dump()
	##obj1.events.sort_by_layer()
	##obj1.events.dump()
	##obj1.events.sort_by_start()
	##obj1.events.dump()
	##obj1.events.sort_by_end()
	##obj1.events.dump()
	##obj1.events.sort_by_style()
	##obj1.events.dump()
	##obj1.events.sort_by_name()
	##obj1.events.dump()
	
	##obj2 = AssParse(filename2, coding)
	###obj2.file_dump()
	##obj2.script_info.dump()
	##obj2.styles.dump()
	##obj2.events.dump()
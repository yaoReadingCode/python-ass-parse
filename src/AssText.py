#!/usr/bin/env python
# coding: utf-8

import re

BLOCK = [  'BLOCK_BASE',
				'BLOCK_PLAIN',
				'BLOCK_OVERRIDE',
				'BLOCK_DRAWING' ]
BLOCK_DICT = dict([(c, i) for i, c in enumerate(BLOCK)]) 

#enum ASS_ParameterClass {
#	PARCLASS_NORMAL,
#	PARCLASS_ABSOLUTE_SIZE,
#	PARCLASS_ABSOLUTE_POS_X,
#	PARCLASS_ABSOLUTE_POS_Y,
#	PARCLASS_RELATIVE_SIZE_X,
#	PARCLASS_RELATIVE_SIZE_Y,
#	PARCLASS_RELATIVE_TIME_START,
#	PARCLASS_RELATIVE_TIME_END,
#	//PARCLASS_RELATIVE_TIME_START_CENTI,
#	//PARCLASS_RELATIVE_TIME_END_CENTI,
#	PARCLASS_KARAOKE,
#	PARCLASS_DRAWING
#};
class AssOverrideParameter:
	"""
	"""
	def __init__(self, data):
		self.parmeter = None
		self.parse()
	
	def parse(self, data):
		pass
	
class AssOverrideTag:
	"""
	
	"""
	def __init__(self, data):
		self.name = None
		self.parameters = []
		self.parse(data)
		
	def parse(self):
		pass

class AssBlockBase:
	"""
	AssBlockBase
	"""
	def __init__(self, text=None):
		#self.type = BLOCK_DICT['BLOCK_BASE']
		if not text:
			self.reset()
		else:
			self.set(text)

	def set(self, text):
		self.text = text
		self.parse()
		
	def reset(self):
		self.text = ''
	
	def parse(self):
		raise Exception('Need override it here!')
	

class AssBlockOverride(AssBlockBase):
	"""
	
	"""
	def __init__(self, text):
		self.tags = []
		AssBlockBase.__init__(self, text)
		self.type = BLOCK_DICT['BLOCK_OVERRIDE']

	def parse(self):
		self.parse_tag()

	def parse_tag(self):
		pass
	
	def get_text(self):
		"""
		get text from self.tags
		"""
		pass
	
	

class AssBlockDrawing(AssBlockBase):
	"""

	"""
	def __init__(self, text):
		AssBlockBase.__init__(self, text)
		self.type = BLOCK_DICT['BLOCK_DRAWING']

	def parse(self):
		pass

class AssBlockPlain(AssBlockBase):
	"""
	plaintext
	"""
	def __init__(self, text):
		AssBlockBase.__init__(self, text)
		self.type = BLOCK_DICT['BLOCK_PLAIN']

	def parse(self):
		pass

class AssText:
	"""
	AssText
	Ass字幕文本类， 包含tag
	"""
	def __init__(self, text = None):
		"""
		init
		"""
		self.blocks = []
		if not text:
			self.reset()
		else:
			self.set(text)
	
	def set(self, text):
		"""
		1. set internal data text
		2. parse  internal data text
		"""
		self.text = text
		self.parse(self.text)
	
	def reset(self):
		self.text = ''
	
	def parse(self, text):
		"""
		parse ass tag
		"""		
		pattern = r'\{?[^\}\{]+\}?'
		text_list = re.findall(pattern, text)
		#print '----------------------------------------------------------------'
		#for item in text_list:
		#	print item.encode('utf-8'),
		#print '----------------------------------------------------------------'
		
		drawing_level = 0
		for work in text_list:
			if work[0] == '{' and work[-1] == '}':
				if work.find('\\'):
					block = AssBlockOverride(work[1:-1])
					self.blocks.append(block)
					for tag in block.tags:
						if tag.name == '\\p':
							drawing_level = int(tag.params[0])
				else:
					#override block with no backslashes
					#here we assume it as a comment text and not consider it an override block
					self.blocks.append( AssBlockPlain(work[1:-1]) )
			elif drawing_level != 0:
				block = AssBlockDrawing(work)
				self.blocks.append(block)
			else:
				block = AssBlockPlain(work)
				self.blocks.append(block)
				
	def tag_strip(self, tagname=None):
		"""
		strip the specific tags
		if key == None, strips all
		"""
		text = ''
		for i in range(len(self.blocks)):
			
			if self.blocks[i].type == BLOCK_DICT['BLOCK_OVERRIDE']:
				if not tagname:	#strip all of the tags
					self.blocks[i].pop(i)
				else:	#strip the specific tag
					for tag in self.blocks[i].tags:
						temp = ''
						if tag.name != tagname:
							temp += 
							
					#self.blocks[i].pop(i)
						
			else:
				text += self.blocks[i].text

	def update_data(self):
		pass

		
def _test_AssText():
	"""
	test case
	"""
	print 'AssText Test:'
	
	file = '../test_subs/ass_text.txt'
	coding = 'utf-8'
	
	f = AssFile(file, coding)
	
	for i in range(len(f.lines)):
		obj = AssText(f.lines[i])
		#print obj.text.encode('utf-8')


if __name__ == "__main__":
	
	from AssFile import *

	_test_AssText()


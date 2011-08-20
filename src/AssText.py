#!/usr/bin/env python
# coding: utf-8

import re
from AssException import *

_Block_Tuple = (
	'BLOCK_BASE',
	'BLOCK_PLAIN',
	'BLOCK_OVERRIDE',
	'BLOCK_DRAWING',
	)
BLOCK_DICT = dict([(c, i) for i, c in enumerate(_Block_Tuple)])

_Ass_Parameter_Type_Tuple = (
	'NORMAL',
	'ABSOLUTE_SIZE',
	'ABSOLUTE_POS_X',
	'ABSOLUTE_POS_Y',
	'RELATIVE_SIZE_X',
	'RELATIVE_SIZE_Y',
	'RELATIVE_TIME_START',
	'RELATIVE_TIME_END',
	'KARAOKE',
	'DRAWING',
	)
PARAM_TYPE_DICT = dict([(c, i) for i, c in enumerate(_Ass_Parameter_Type_Tuple)])

Ass_Parameter_Name = (
	#\b<0 or 1>
	u'\\b',
	#\i<0 or 1>
	u'\\i',
	#\u<0 or 1>
	u'\\u',
	#\s<0 or 1>
	u'\\s',
	#\bord<width>
	u'\\bord',
	#\shad<depth>
	u'\\shad',
	#\be<0 or 1>
	u'\\be',
	#\fn<font name>
	u'\\fn',
	#\fs<font size>
	u'\\fs',
	#\fsc<x or y><percent>
	u'\\fsc',
	#\fsp<pixels >
	u'\\fsp',
	#\fr[<x/y/z>]<degrees>
	u'\\fr',
	#\fe<charset>
	u'\\fe',
	#\c&H<bbggrr>&
	u'\\c',
	#\a<alignment>
	u'\\a',
	#\an<alignment>
	u'\\an',
	#\k<duration>
	u'\\k',
	#\q<num>
	u'\\q',
	#\r[<style>]
	u'\\r',
##Functions:
	#\t([<t1>, <t2>, ] [<accel>,] <style modifiers>)
	u'\\t',
	#\move(<x1>, <y1>, <x2>, <y2>[, <t1>, <t2>])
	u'\\move',
	#\pos(<x>, <y>)
	u'\\pos',
	#\org(<x>, <y>)
	u'\\org',
	#\fade(<a1>, <a2>, <a3>, <t1>, <t2>, <t3>, <t4>)
	u'\\fade',
	#\fad(<t1>, <t2>)
	u'\\fad',
	#\clip(<x1>, <y1>, <x2>, <y2>)
	u'\\clip',
	#\clip([<scale>,] <drawing commands>)
	u'\\clip',
##Drawings:
	#\p<scale>
	u'\\p',
	#\pbo<y>
	u'\\pbo',
)


class AssOverrideParameter:
	"""
	"""
	def __init__(self, data):
		self.parameter = None
		self.type = PARAM_TYPE_DICT['NORMAL']
		self.parse(data)
	
	def parse(self, data):
		pass
	
class AssOverrideTag:
	"""
	
	"""
	def __init__(self, data):
		self.invaild = False
		self.name = None		#tag name
		self.parameters = []		#tag parameters
		self.parse(data)
		
	def parse(self, data):
		for name in Ass_Parameter_Name:
			if data[:len(name)] == name:
				#get the vaild tag name
				self.name = name
				try:
					param = AssOverrideParameter(data[len(name):])
				except InvaildDataError:
					raise Exception('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\r\n\r\n')
			else:
				self.name = data
				self.invaild = False
				
			
		self.invaild = True		#if invaild, set it as True, or else False

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
	AssBlockOverride
	"""
	def __init__(self, text):
		self.tags = []
		AssBlockBase.__init__(self, text)
		self.type = BLOCK_DICT['BLOCK_OVERRIDE']

	def parse(self):
		self.parse_tag()

	def parse_tag(self):
		del self.tags[:]
		#pattern = r'\\([^\]+)'
		split_list = self.text.split('\\')		#split all tags, if exists
		#print split_list
		#print '--------------------------------------------'
		#print '--------------------------------------------'
		for split_item in split_list:
			split_item_strip = split_item.strip()
			if split_item_strip:
				split_item_strip = '\\' + split_item_strip
				while split_item_strip.count('(') > split_item_strip.count(')'):
					split_item_strip += ')'
					#raise Exception('xxxxx')
					print 'Warnning: parenthesis mismatch here!'
				try:
					tag = AssOverrideTag(split_item_strip)
					print split_item_strip.encode('utf-8')
					#print '--------------------------------------------'
				except InvaildDataError, msg:
					print 'parse tag failed!'
					print InvaildDataError, ':', msg
				else:
					self.tags.append(tag)
			#else: blank string is ignored here
		
	
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
							pass #temp += 
							
					#self.blocks[i].pop(i)
						
			else:
				text += self.blocks[i].text

	def update_data(self):
		"""
		update internal data self.text from self.tags
		"""
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


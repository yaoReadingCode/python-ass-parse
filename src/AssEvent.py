#!/usr/bin/env python
# coding: utf-8

from AssException import *
from AssEntry import *
from AssTime import *
from AssText import *

class AssEntryDialogue(AssEntry):
	"""
	AssDialogue类
	实现[Events] Section中的Dialogue项目存储和操作
	"""
	def __init__(self, data, section, version):
		AssEntry.__init__(self, data, section)
		self.type = ENTRY_DIALOGUE
		self.reset()
		self.comment = False
		self.need_update = False
		self.parse(self.data, version)

	def reset(self):
		"""
		init internal data here
		Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
		"""
		self.layer = 0
		self.start = AssTime()
		self.end = AssTime()
		self.style = ''
		self.name = ''
		self.marginl = 0
		self.marginr = 0
		self.marginv = 0
		self.effect = ''
		self.text = AssText()
		
		#self.layer, self.start, self.end, self.style, self.name, self.marginl, self.marginr, self.marginv, self.effect, self.text
		
	def get_type(self):
		return ENTRY_DIALOGUE
		
	def parse(self, line, version):
		try:
			event_list = line.split(':', 1)
			
			if event_list[0].lower() == 'dialogue':
				self.comment = False
			elif event_list[0].lower() == 'comment':
				self.comment = True
			else:
				#self.reset()	
				raise InvaildDataError('Invaild Data <%s>' % (line) )
				return
			
			event_list = event_list[1].split(',', 9)
			i = 0
			if version == 0 or event_list[i].strip().startswith('marked'):
				self.layer = 0
			else:
				self.layer = int(event_list[i])		#0
			
			i += 1; self.start.set(event_list[i].strip())	#1
			i += 1; self.end.set(event_list[i].strip())	#2
			i += 1; self.style = event_list[i].strip()		#3
			i += 1; self.name = event_list[i].strip()	#4
			i += 1; self.marginl = int(event_list[i])		#5
			i += 1; self.marginr = int(event_list[i])		#6
			i += 1; self.marginv = int(event_list[i])	#7
			i += 1; self.effect = event_list[i].strip()	#8
			i += 1; self.text.parse(event_list[i])	#9
		except IndexError, msg:
			print IndexError, ':', msg
		else:
			pass
	
	def form_data(self):
		"""
		根据tag信息生成数据，并直接返回
		Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
		"""
		return '%s: %d,%s,%s,%s,%s,%04d,%04d,%04d,%s,%s' % \
				(
					self.comment and 'Comment' or 'Dialogue',
					self.layer, 
					self.start.get_ass_formated_time(), 
					self.end.get_ass_formated_time(), 
					self.style, 
					self.name, 
					self.marginl, self.marginr, self.marginv, 
					self.effect, 
					self.text.text
				)
		
	def update_data(self):
		"""
		根据tag信息更新data数据
		"""
		self.data = self.form_data()
		

class AssEvents:
	"""
	AssEvent
	"""
	def __init__(self):
		self.events = []
		self.format = AssEntry('', '[Events]')
		self.trueversion = -1
		
	def parse(self, line, version):
		if line.startswith('Format:'):
			self.format.set_data('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')
		#elif line.startswith('Dialogue:'):
		
		if line.startswith('Format:'):
			try:
				low_format_str = line.split(':', 1)[1].strip().lower()
				if low_format_str.startswith('marked'):		#SSA style
					self.trueversion = 0
				elif low_format_str.startswith('layer'):		#ASS V4.0+
					self.trueversion = 1
				else:
					self.trueversion = version
			except IndexError, msg:
				print IndexError, ':', msg

			self.format.set_data('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')
					
		elif line.startswith('Dialogue:') or line.startswith('Comment:'):
			try:
				event = AssEntryDialogue(line, '[Events]', self.trueversion)
			except UnknowDataError, err_msg:
				print UnknowDataError, ':', err_msg
			else:
				self.events.append(event)
				
		elif line:
			raise UnknowDataError('Unknow Data <%s>' % (line))
			
	def sort(self, reverse=False):
		"""
		sort by text
		"""
		pass
		#self.events.sort(cmp=lambda x,y: cmp(x.text.text, y.text.text), reverse=reverse)
		
	def sort_by_layer(self, reverse=False):
		"""
		sort by layer
		"""
		self.events.sort(cmp=lambda x,y: cmp(x.layer, y.layer), reverse=reverse)
		
	def sort_by_start(self, reverse=False):
		"""
		sort by start time
		"""
		self.events.sort(cmp=lambda x,y: cmp(x.start.time, y.start.time), reverse=reverse)

	def sort_by_end(self, reverse=False):
		"""
		sort by end time
		"""
		self.events.sort(cmp=lambda x,y: cmp(x.end.time, y.end.time), reverse=reverse)

	def sort_by_style(self, reverse=False):
		"""
		sort by end style
		"""
		self.events.sort(cmp=lambda x,y: cmp(x.style.lower(), y.style.lower()), reverse=reverse)

	def sort_by_name(self, reverse=False):
		"""
		sort by end name
		"""
		self.events.sort(cmp=lambda x,y: cmp(x.name.lower(), y.name.lower()), reverse=reverse)
		
	def dump(self):
		print ('================== ASS Event Dump Begin ===================')
		print '[Events]'
		print self.format.data
		#for i in range(len(self.events)):
			#self.events[i].dump()
		for i in range(len(self.events)):
			print self.events[i].form_data().encode('utf-8')
			#self.events[i].dump()
		print ('=================== ASS Event Dump End ====================')

def _test_AssEvent():
	"""
	test case
	"""
	print 'AssEvent Test:'

if __name__ == "__main__":
	_test_AssEvent()

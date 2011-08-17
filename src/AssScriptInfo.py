#!/usr/bin/env python
# coding: utf-8

from AssEntry import *
from AssException import *

class AssEntryInfo(AssEntry):
	"""
	AssInfo类
	实现[Script Info] Section中的项目存储和操作
	Note: Script Info以字典的形式存储
	"""
	def __init__(self, data, section):
		AssEntry.__init__(self, data, section)
		self.type = ENTRY_SCRIPT_INFO
		self.reset()
		self.need_update = False		#if need update self.data from internal data
		self.parse()

	def reset(self):
		"""
		init internal data here
		"""
		self.title = None
		self.content = None

	def get_type(self):
		return ENTRY_SCRIPT_INFO

	def parse(self):
		"""
		解析文本为内部数据
		#Title:
		#Original Script:
		#Original Translation:
		#Original Editing:
		#Original Timing:
		#Synch Point:
		#Script Updated By:
		#Update Details:
		#Script Type:
		#ScriptType:
		#Collisions:
		#PlayResY:
		#PlayResX:
		#PlayDepth:
		#Timer:
		#WrapStyle:
		#ScaledBorderAndShadow:
		"""
		if self.data is None:
			self.item = {}
			return
		elif self.data[0] == u';':
			#it was just a comment line, should raise exception here!
			print 'comment line found: should raise exception here!'
		
		item = self.data.split(':', 1)

		try:
			#strip
			item[0] = item[0].strip()
			item[1] = item[1].strip()
		except IndexError, err_msg:
			print IndexError, ':', err_msg		#无效索引

		else:
			if item[0].lower() == Title.lower():	#start with "Title:"
				self.title = item[0]	#提取Title后的文本
				self.content = item[1]
				#self.item[item[0]] = item[1]
			elif item[0].lower() == OriginalScript.lower():	#start with "OriginalScript"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == OriginalTranslation.lower():	#start with "OriginalTranslation"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == OriginalEditing.lower():	#start with "OriginalEditing"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == OriginalTiming.lower():	#start with "OriginalTiming"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == SynchPoint.lower():	#start with "SynchPoint"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == ScriptUpdatedBy.lower():	#start with "ScriptUpdatedBy"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == UpdateDetails.lower():	#start with "UpdateDetails"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == ScriptType.lower():	#start with "ScriptType"
				self.title = item[0]	#Script Type 1, start with "Script Type:"
				self.content = item[1]
			elif item[0].lower() == ScriptType2.lower():	#start with "ScriptType2"
				self.title = item[0]	#Script Type 2, start with "ScriptType:"
				self.content = item[1]
			elif item[0].lower() == Collisions.lower():	#start with "Collisions"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == PlayResY.lower():	#start with "PlayResY"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == PlayResX.lower():	#start with "PlayResX"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == PlayDepth.lower():	#start with "PlayDepth"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == Timer.lower():	#start with "Timer"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == WrapStyle.lower():	#start with "WrapStyle"
				self.title = item[0]	#提取文本
				self.content = item[1]
			elif item[0].lower() == ScaledBorderAndShadow.lower():	#start with "ScaledBorderAndShadow"
				self.title = item[0]	#提取文本
				self.content = item[1]
			else:
				raise UnknowDataError('Unknow Data <%s>' % (self.data) )
				#print ("Warnning: Unknow Data: '%s'" % (self.data) )

	def form_data(self):
		"""
		根据内部信息生成数据，并直接返回
		"""
		return 

	def update_data(self):
		"""
		根据内部信息更新data数据
		"""
		pass

	
class AssScriptInfo:
	"""
	AssScriptInfo
	"""
	def __init__(self):
		self.script_info = []
		
	def parse(self, line):
		try:
			info = AssEntryInfo(line, '[Script Info]')
		except UnknowDataError, err_msg:
			print Exception, ':', err_msg
		else:
			self.script_info.append(info)
			
	def dump(self):
		print ('================= Script Info Dump Begin ==================')
		print '[Script Info]'
		for i in range(len(self.script_info)):
			self.script_info[i].dump()
		print ('================== Script Info Dump End ===================')
		
def _test_AssScriptInfo():
	"""
	test case
	"""
	print 'AssScriptInfo Test:'

if __name__ == "__main__":
	_test_AssScriptInfo()

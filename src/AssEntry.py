#!/usr/bin/env python
# coding: utf-8

from AssDataType import *

class AssEntry:
	"""
	AssEntry类
	实现基本的数据存储和操作
	"""
	def __init__(self, data='', section=''):
		"""
		data: 存储的raw数据, 以unicode字符串形式存储, 头尾空白已去除
		type: Entry类型
		section: Ass section 标志
		"""
		self.set_data(data)

		self.type = ENTRY_BASE
		if not section:
			self.section = ''
		else:
			self.section = section
	
	def set_data(self, new_data):
		"""
		set self.data as new_data
		"""
		data = new_data.strip()
		try:
			if not data:
				self.data = ''
			else:
				self.data = data.strip()		#去除头尾空白
		except:
			print 'Exception is catched: data type is invaild!'
			self.data = ''
	
	def dump(self, encoding = 'utf-8'):
		"""
		dump internal data
		"""
		#print self.data.encode('utf-8')
		print self.data.encode(encoding)

def _test_AssEntry():
	"""
	test case
	"""
	print 'AssEntry Test:'

if __name__ == "__main__":
	_test_AssEntry()

#!/usr/bin/env python
# coding: utf-8

import codecs
class FileBase:
	"""
	提供基本的文件操作功能
	filename: 文件名
	encoding: 文件的编码格式, 如'utf-8', 'gb2312'
	"""
	def __init__(self, filename, encoding):
		"""
		读取文件
		"""
		self.reset()
		self.filename = filename		#文件名
		self.encoding = encoding	#文件编码
		self.__read_file(filename, encoding)

	def __read_file(self, filename, encoding):
		"""
		read file
		Note: 
			1. utf-8 bom need to be handled here!
			2. if needed, line_handle() could be override
		"""
		try:
			f = codecs.open(filename, 'r', encoding)
			lines = f.readlines()
			for i in range(len(lines)):
				self.line_handle(lines[i])
		except IOError, err_msg: 
			print IOError, ':', err_msg
			self.filename = ''
		#except:
		#	pass
		else:
			print 'open file success!'
		finally:
			f.close()

	def line_handle(self, line):
		"""
		单行处理
		"""
		#在这里进行特殊处理
		self.lines.append(line)

	def reset(self):
		self.lines = []

	def reload_file(self, encoding=''):
		"""
		以指定的编码重新加载文件
		"""
		if encoding:
			self.encoding = encoding
		
		self.__init__(self.filename, self.encoding)

	def save(self, encoding=''):
		"""
		save file as self.filename
		"""
		if not encoding:
			encoding = self.encoding
		
		self.save_as(self.filename, encoding)

	def save_as(self, filename, encoding=''):
		"""
		save file as specific filename
		"""
		if not encoding:
			encoding = self.encoding

		pass
		
	def file_dump(self):
		for i in range(len(self.lines)):
			print self.lines[i].encode('gb2312')
	
class SrtFile(FileBase):
	"""
	提供Srt文件操作功能
	"""
	pass

class AssFile(FileBase):
	"""
	提供Ass文件操作功能
	filename: 文件名
	encoding: 文件的编码格式, 默认为utf-8
	"""
	def __init__(self, filename, encoding='utf-8'):
		"""
		读取文件
		"""
		self.reset()
		FileBase.__init__(self, filename, encoding)
			
	def line_handle(self, line):
		"""
		单行处理：去除空白行和注释行
		"""
		tmp = line.strip()
		if not tmp or tmp.startswith(';'):
			return
		if tmp:
			self.lines.append(tmp)

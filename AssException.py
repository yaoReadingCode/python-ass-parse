#!/usr/bin/env python
# coding: utf-8

class UnknowDataError(Exception):
	"""
	未知数据
	"""
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class InvaildDataError(Exception):
	"""
	非法数据
	"""
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

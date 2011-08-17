#!/usr/bin/env python
# coding: utf-8

class AssTime:
	"""
	AssTime
	"""
	def __init__(self, time = None):
		"""
		init AssTime
		"""
		if not time:
			self.reset()
		else:
			self.set(time)
	
	def set(self, time):
		if type(time) == type(int):
			self.time = time
		else:
			self._parse(time.strip())
			
	def reset(self):
		self.time = 0
	
	def _parse(self, time):
		"""
		parse ass/srt time
		
		ass/ssa time format as:	0:00:03.00
		srt time format as:	00:00:03,000
		"""
		except_raise = False
		try:
			time_list = time.split(':')
			th = int(time_list[0])
			tm = int(time_list[1])
			
			time_list_2 = time_list[2].split(',')
			if len(time_list_2) == 2:
				ts = int(time_list_2[0])
				tms = int(time_list_2[1])
			else:
				time_list_2 = time_list[2].split('.')
				if len(time_list_2) == 2:
					ts = int(time_list_2[0])
					tms = int(time_list_2[1]) * 10
		except IndexError:
			except_raise = True
			
		if except_raise is True:
			self.time = 0
			raise InvaildDataError('Invaild Data <%s>' % (time) )
		else:
			#print 'parse time:', th, tm, ts, tms
			self.time = th*3600000 + tm*60000 + ts*1000 + tms

	def get_ass_formated_time(self):
		"""
		Note: 
		"""
		time = self.__get_sep_time()
		return '%01d:%02d:%02d.%02d' % (time[0], time[1], time[2], int(time[3]/10))
		
		
		
	def get_ssa_formated_time(self):
		time = self.__get_sep_time()
		return '%01d:%02d:%02d.%02d' % (time[0], time[1], time[2], int(time[3]/10))

	def get_srt_formated_time(self):
		
		time = self.__get_sep_time()
		return '%01d:%02d:%02d,%03d' % (time[0], time[1], time[2], time[3])
		
	def __get_sep_time(self):
		"""
		get separated time
		"""
		_ms = self.time
		
		th = int(_ms / 3600000)
		_ms = _ms % 3600000
		
		tm = int(_ms / 60000)
		_ms = _ms % 60000
		
		ts = int(_ms / 1000)
		_ms = _ms % 1000
		
		tms = _ms
		
		return (th, tm, ts, tms)

def _test_AssTime():
	"""
	test case
	"""
	print 'AssTime Test:'

if __name__ == "__main__":
	_test_AssTime()

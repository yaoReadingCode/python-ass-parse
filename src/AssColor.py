#!/usr/bin/env python
# coding: utf-8

class AssColor:
	"""
	Ass Color
	RGB&Alpha
	"""
	def __init__(self, color = None):
		"""
		init AssColor
		
		self.r	#red
		self.g	#green
		self.b	#blue
		self.a	#alpha
		"""
		if not color:
			self.reset()
		else:
			self.set(color)
			
	def set(self, color):
		self._parse(color)
		
	def reset(self):
		(self.r, self.g, self.b, self.a) = (0, 0, 0, 0)
		
	def _parse(self, color):
		"""
		parse ass/srt color
		
		######///TODO:
		color format &HAABBGGRR
		ass color format as:  &H00FFFFFF
		ssa color format as:  &Hffffff
		srt/html color format as: #990000
		srt color format as: {\3c&Hd22c255&} or {\2c&Hd22c125&}
		"""
		#re.search(r'&H([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2}?)&?', u'&H00FFFFFF&').groups()
		except_raise = False
		low_color = color.lower()
		if low_color.startswith('&h'):
			length = len(low_color)
			try:
				if length == 10:
					#	&HAABBGGRR
					alpha = int(low_color[2:4], 16)
					blue = int(low_color[4:6], 16)
					green = int(low_color[6:8], 16)
					red = int(low_color[8:10], 16)
				elif length == 8:
					# &HBBGGRR
					alpha = 0
					blue = int(low_color[2:4], 16)
					green = int(low_color[4:6], 16)
					red = int(low_color[6:8], 16)
			except:
				except_raise = True
		else:
			except_raise = True
		
		if except_raise is False:
			(self.r, self.g, self.b, self.a) = (red, green, blue, alpha)
		else:
			(self.r, self.g, self.b, self.a) = (0, 0, 0, 0)
			raise InvaildDataError('Invaild Data <%s>' % (color) )

	def get_ass_formated_color(self):
		return '&H%02X%02X%02X%02X' % (self.a, self.b, self.g, self.r)
		
	def get_ssa_formated_color(self):
		return '&H%02X%02X%02X%02X' % (self.a, self.b, self.g, self.r)

	def get_srt_formated_color(self):
		pass
		
def _test_AssColor():
	"""
	test case
	"""
	print 'AssColor Test:'

if __name__ == "__main__":
	_test_AssColor()

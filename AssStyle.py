#!/usr/bin/env python
# coding: utf-8

from AssEntry import *
from AssException import *

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

class AssEntryStyle(AssEntry):
	"""
	AssStyle类
	实现[Stlyes] Section中的Stlye项目存储和操作
	
V4.0+ Format:
		Name, Fontname, Fontsize, 		#3
		PrimaryColour, SecondaryColour, OutlineColour, BackColour, 	#4
		Bold, Italic, 		#2
		Underline, StrikeOut, 	#2
		ScaleX, ScaleY, Spacing, Angle, 		#4
		BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, 	#7
		Encoding		#1
		
V4.0 Format:
		Name, Fontname, Fontsize, 		#3
		PrimaryColour, SecondaryColour, TertiaryColour, BackColour, 		#4
		Bold, Italic, 		#2
								#0
								#0
		BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, 		#7
		AlphaLevel, 			#1
		Encoding			#1
	"""
	def __init__(self, data, section, version):
		AssEntry.__init__(self, data, section)
		self.type = ENTRY_STYLE
		self.reset()
		self.need_update = False
		self.parse(self.data, version)
		
	def reset(self):
		"""
		reset internal data here
		Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, 
		ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
		"""
		#['Format','Name','Fontname','Fontsize','PrimaryColour','SecondaryColour','OutlineColour','BackColour','Bold','Italic',
		#'Underline','StrikeOut','ScaleX','ScaleY','Spacing','Angle','BorderStyle','Outline','Shadow','Alignment','MarginL','MarginR','MarginV','Encoding']
		
		self.name = ''
		self.fontname = ''
		self.fontsize = ''
		
		self.primary_color = AssColor()
		self.secondary_color = AssColor()
		self.outline_color = AssColor()
		self.back_color = AssColor()
		
		self.bold = False
		self.italic = False
		self.underline = False
		self.strikeout = False
		
		self.scalex = 0	#Modifies the width of the font. [percent]
		self.scaley = 0	#Modifies the height of the font. [percent]
		self.spacing = 0	#Extra space between characters. [pixels]
		self.angle = 0.0	#The origin of the rotation is defined by the alignment. Can be a floating point number. [degrees]
		self.borderstyle = 0
		self.outline = 0
		self.shadow = 0
		self.alignment = 0
		self.margin_l = 0
		self.margin_r = 0
		self.margin_v = 0
		self.encoding = 0

	def get_type(self):
		return ENTRY_STYLE

	def parse(self, line, version):
		"""
		parse ass style here
		Note:
			1. 
		"""
		try:
			style_list = line.split(':', 1)
			
			if style_list[0].lower() != 'style':
				#self.reset()
				raise InvaildDataError('Invaild Data <%s>' % (line) )
				return
			
			style_list = style_list[1].split(',')
			
			#parse
			i = 0;		self.name = style_list[i].strip()		#0
			i += 1;	self.fontname = style_list[i].strip()		#1
			i += 1;	self.fontsize = int(style_list[i])		#2
			
			i += 1;	self.primary_color.set(style_list[i].strip())	#3
			i += 1;	self.secondary_color.set(style_list[i].strip())	#4
			i += 1;	self.outline_color.set(style_list[i].strip())		#5
			i += 1;	self.back_color.set(style_list[i].strip())		#6
			if version is 0:
				#SSA uses BackColour for both outline and shadow, this will destroy SSA's TertiaryColour
				self.outline_color= self.back_color	#ssa color

			i += 1;	self.bold = int(style_list[i]) and True or False		#7
			i += 1;	self.italic = int(style_list[i]) and True or False		#8

			if version is not 0:
				i += 1;	self.underline = int(style_list[i]) and True or False	#9
				i += 1;	self.strikeout = int(style_list[i]) and True or False	#10
				i += 1;	self.scalex = float(style_list[i])			#11
				i += 1;	self.scaley = float(style_list[i])			#12
				i += 1;	self.spacing = float(style_list[i])			#13
				i += 1;	self.angle = float(style_list[i])			#14
			else:
				self.underline = False;
				self.strikeout = False;
				self.scalex = 100;
				self.scaley = 100;
				self.spacing = 0;
				self.angle = 0.0;		
		
			i += 1;	self.borderstyle = int(style_list[i])	#15    /    #15-6 for ssa
			i += 1;	self.outline = int(style_list[i])		#16    /    #16-6 for ssa
			i += 1;	self.shadow = int(style_list[i])		#17    /    #17-6 for ssa
			i += 1;	self.alignment = int(style_list[i])		#18    /    #18-6 for ssa
			i += 1;	self.margin_l = int(style_list[i])		#19    /    #19-6 for ssa
			i += 1;	self.margin_r = int(style_list[i])		#20   /    #20-6 for ssa
			i += 1;	self.margin_v = int(style_list[i])		#21    /    #21-6 for ssa
			#Note: 如果是version=2, 即v4.0++ 则包含4个margin参数
			#TODO:
			if version is 2:
				i += 1; self.margin_4 = int(style_list[i])		#22

			if version is 0:
				i += 1
				i += 1;	self.encoding = int(style_list[i])	#23-6 for ssa
			else:
				i += 1;	self.encoding = int(style_list[i])	#22    /     #23 for ass v4.0++
			
		except IndexError, msg:
			print IndexError, ':', msg
			return
		else:
			pass
		
	def form_data(self):
		"""
		根据tag信息生成数据，并直接返回
		"""
		return 'Style: %s,%s,%d,%s,%s,%s,%s,%d,%d,%d,%d,%g,%g,%g,%.2f,%d,%d,%d,%d,%d,%d,%d,%d' % \
					(self.name, self.fontname, self.fontsize,
						self.primary_color.get_ass_formated_color(),
						self.secondary_color.get_ass_formated_color(),
						self.outline_color.get_ass_formated_color(),
						self.back_color.get_ass_formated_color(),
						self.bold and -1 or 0, 
						self.italic and -1 or 0, 
						self.underline and -1 or 0, 
						self.strikeout and -1 or 0,
						self.scalex, self.scaley, self.spacing, self.angle, self.borderstyle,
						self.outline, self.shadow, self.alignment, self.margin_l, self.margin_r, self.margin_v, self.encoding
					)
		
		
	def update_data(self):
		"""
		根据tag信息更新data数据
		"""
		self.data = self.form_data()

class AssStyles:
	"""
	AssEntryStyle
	"""
	def __init__(self):
		self.styles = []
		self.format = AssEntry('', '[Styles]')
		self.trueversion = -1
		
	def parse(self, line, version):
		if line.startswith('Format:'):
			try:
				item_list = line.split(':', 1)[1].split(',')
				#print item_list
				length = len(item_list)
				if length == 18:	#v4.0
					self.trueversion = 0
				elif length == 23:	#v4.0+
					self.trueversion = 1
				else:
					self.trueversion = version
			except IndexError, msg:
				print IndexError, ':', msg

			self.format.set_data('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding')
					
		elif line.startswith('Style:'):
			try:
				style = AssEntryStyle(line, '[Styles]', self.trueversion)
			except UnknowDataError, err_msg:
				print UnknowDataError, ':', err_msg
			else:
				self.styles.append(style)
		elif line:
			raise UnknowDataError('Unknow Data <%s>' % (line))
			
	def dump(self):
		print ('================== ASS Style Dump Begin ===================')
		print '[Styles]'
		print self.format.data.encode('utf-8')
		#for i in range(len(self.styles)):
			#self.styles[i].dump()
		for i in range(len(self.styles)):
			print self.styles[i].form_data().encode('utf-8')
			#self.styles[i].dump()
		print ('=================== ASS Style Dump End ====================')

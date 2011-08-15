#!/usr/bin/env python
# coding: utf-8
"""
    Python Ass Parser
"""

#import os
#import sys
#import string
import re
Section_ScriptInfo=u'[Script Info]'
Section_V4P_Styles=u'[V4+ Styles]'
Section_V4_Styles=u'[V4 Styles]'
Section_Events=u'[Events]'

Title='Title'#标题, 如果没有提供, 则自动使用<untitled>
OriginalScript='Original Script'#剧本的最初作者, 若没有提供则自动使用<unknown>
OriginalTranslation='Original Translation'#(可选)原剧本的翻译者, 若没有提供则该行不显示
OriginalEditing='Original Editing'#(可选)原剧本的编者和校对, 若没有提供则该行不显示
OriginalTiming='Original Timing'#(可选)原剧本的时间轴人员, 若没有提供则该行不显示
SynchPoint='Synch Point'#(可选)从哪个时间点开始加载字幕, 若没有提供则该行不显示
ScriptUpdatedBy='Script Updated By'#(可选)对原剧本的修改/更新人员, 若没有提供则该行不显示
UpdateDetails='Update Details'#更新的具体信息, 若没有提供则该行不显示
ScriptType='Script Type'#SSA的版本信息, SSA的版本一般为v4.00，ASS的版本为”v4.00+”
ScriptType2='ScriptType'#ASS的版本信息, SSA的版本一般为v4.00，ASS的版本为”v4.00+”
Collisions='Collisions'#当字幕时间重叠时, 前后字幕的堆叠方式.
#值为”Normal”时, 后一条字幕出现在前一条字幕的上方.
#如果值为”Reverse”时, 前一条字幕往上移动给后一条字幕让位.
PlayResY='PlayResY'#文件所使用的视频高度参考标准, 如果使用Directdraw回放SSA v4会自动选择最相近的启用的设置
PlayResX='PlayResX'#文件所使用的视频宽度参考标准, 如果使用Directdraw回放SSA v4会自动选择最相近的启用的设置.
#如果只提供了PlayResX, PlayResY其中一种, 那另一种会按实际视频的像素值为准.
#提供的分辨率数值影响以下参数
#1) 所有给出的坐标(到边缘的距离, \pos, \move, 矢量绘图等)都以此分辨率作为参照.
#2) 所有的文字字号均按照此分辨率等比例放大缩小
#3) 当ScaledBorderAndShadow被启用时, 所有边框宽度和阴影深度都按照此分辨率与实际分辨率的比例等比例缩放
#4) 这个分辨率不影响最终显示文字的宽高比, 但影响矢量绘画图形的宽高比.
PlayDepth='PlayDepth'#加载字幕时使用的色深(颜色的数目), 如果使用Directdraw回放SSA v4会自动选择最相近的启用的设置
Timer='Timer'#字幕加载的速度调整, 数值为百分数. 例如”100.0000″代表100%. 其数值有4位小数点.
#它相当于对ASS字幕的时间速度进行乘法运算.
#当速度大于100%时, 总时间会缩短, 而相应的字幕会越来越靠前.
#当速度小于100%时, 总时间会延长, 而相应的字幕会越来越靠后.
WrapStyle='WrapStyle'#定义默认的换行方式,
#0 智能换行, 行分得较平均, 上面的行较长
#1 一行结束后从行尾的词分行
#2 不换行. 此模式下只有\n, \N才换行
#3 与模式0相同, 但下面的行分得比较长
ScaledBorderAndShadow='ScaledBorderAndShadow'#指定边框宽度与阴影深度是否随着视频分辨率等比例缩放. 可为Yes, No. 默认为No.
#当取值为No时, 边框宽度与阴影深度完全按照指定的像素数显示.
#当取值为Yes时, 边框宽度与阴影深度随着实际视频的分辨率同等比例缩放.

Format='Format' #
Style_Name=0
Style_Fontname=1
Style_Fontsize=2
Style_PrimaryColour=3
Style_SecondaryColour=4
Style_OutlineColour=5
Style_BackColour=6
Style_Bold=7
Style_Italic=8
Style_Underline=9
Style_StrikeOut=10
Style_ScaleX=11
Style_ScaleY=12
Style_Spacing=13
Style_Angle=14
Style_BorderStyle=15
Style_Outline=16
Style_Shadow=17
Style_Alignment=18
Style_MarginL=19
Style_MarginR=20
Style_MarginV=21
Style_Encoding=22
Style_Format=['Name','Fontname','Fontsize','PrimaryColour','SecondaryColour','OutlineColour','BackColour',
              'Bold','Italic','Underline','StrikeOut','ScaleX','ScaleY','Spacing','Angle','BorderStyle',
              'Outline','Shadow','Alignment','MarginL','MarginR','MarginV','Encoding']

Event_Layer=0
Event_Start=1
Event_End=2
Event_Style=3
Event_Actor=4
Event_MarginL=5
Event_MarginR=6
Event_MarginV=7
Event_Effect=8
Event_Text=9
Event_Format=['Layer','Start','End','Style','Actor','MarginL','MarginR','MarginV','Effect','Text']

Dialogue='Dialogue'
Comment='Comment'
Picture='Picture'
Sound='Sound'
Movie='Movie'
Command='Command'

#ASS_EntryType 
ENTRY_BASE = 0
ENTRY_SCRIPT_INFO = 1
ENTRY_STYLE = 2
ENTRY_COMMENT = 3
#ENTRY_ATTACHMENT = 4
ENTRY_DIALOGUE = 1000

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

class AssEntryInfo(AssEntry):
	"""
	AssInfo类
	实现[Script Info] Section中的项目存储和操作
	Note: Script Info以字典的形式存储
	"""
	def __init__(self, data, section):
		AssEntry.__init__(self, data, section)
		self.type = ENTRY_SCRIPT_INFO
		self.__init_data()
		self.need_update = False		#if need update self.data from internal data
		self.parse()

	def __init_data(self):
		"""
		init internal data here
		"""
		self.title = ''
		self.content = ''

	def get_type(self):
		return ENTRY_SCRIPT_INFO

	def parse(self):
		"""
		解析文本为内部数据
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
		if color is None:
			(self.r, self.g, self.b, self.a) = (0, 0, 0, 0)
		else:
			parse(color)
			
	def parse(self, color):
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

#"0" <-> "ANSI"
#"1" <-> "Default"
#"2" <-> "Symbol"
#"77" <-> "Mac"
#"128" <-> "Shift_JIS"
#"129" <-> "Hangeul"
#"130" <-> "Johab"
#"134" <-> "GB2312"
#"136" <-> "Chinese BIG5"
#"161" <-> "Greek"
#"162" <-> "Turkish"
#"163" <-> "Vietnamese"
#"177" <-> "Hebrew"
#"178" <-> "Arabic"
#"186" <-> "Baltic"
#"204" <-> "Russian"
#"222" <-> "Thai"
#"238" <-> "East European"
#"255" <-> "OEM"
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
		self.__init_data()
		self.need_update = False
		self.parse(self.data, version)
		
	def __init_data(self):
		"""
		init internal data here
		Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, 
		ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
		"""

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
			style_list = style_list[1].split(',')
			
			#parse
			self.name = style_list[0].strip()
			self.fontname = style_list[1].strip()
			##self.fontsize = style_list[2].strip()
			self.fontsize = int(style_list[2])
			
			if version is 0:				
				self.primary_color.parse(style_list[3].strip())
				self.secondary_color.parse(style_list[4].strip())
				self.outline_color.parse(style_list[6].strip())		##
				self.back_color.parse(style_list[6].strip())		##
			else:
				self.primary_color.parse(style_list[3].strip())
				self.secondary_color.parse(style_list[4].strip())
				self.outline_color.parse(style_list[5].strip())
				self.back_color.parse(style_list[6].strip())	

			self.bold = int(style_list[7]) and True or False
			self.italic = int(style_list[8]) and True or False

			if version is not 0:
				self.underline = int(style_list[9]) and True or False
				self.strikeout = int(style_list[10]) and True or False
				self.scalex = float(style_list[11])
				self.scaley = float(style_list[12])
				self.spacing = float(style_list[13])
				self.angle = float(style_list[14])
			else:
				self.underline = false;
				self.strikeout = false;
				self.scalex = 100;
				self.scaley = 100;
				self.spacing = 0;
				self.angle = 0.0;		
		
			self.borderstyle = int(style_list[15])
			self.outline = int(style_list[16])
			self.shadow = int(style_list[17])
			self.alignment = int(style_list[18])
			self.margin_l = int(style_list[19])
			self.margin_r = int(style_list[20])
			self.margin_v = int(style_list[21])
			#Note: 如果是version=2, 即v4.0++ 则包含4个margin参数
			#TODO:

			if version is 1:
				self.encoding = int(style_list[22])
			elif version is 0:
				self.encoding = int(style_list[23])
			elif version is 2:
				pass
				#TODO:
			
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

class AssEntryDialogue(AssEntry):
	"""
	AssDialogue类
	实现[Events] Section中的Dialogue项目存储和操作
	"""
	def __init__(self, data, section):
		AssEntry.__init__(self, data, section)
		self.type = ENTRY_DIALOGUE
		##self.comment = False
		##self.title = ''
		##self.content = ''
		self.need_update = False
		self.parse()

	def get_type(self):
		return ENTRY_DIALOGUE
		
	def parse(self):
		pass
	
	def form_data(self):
		"""
		根据tag信息生成数据，并直接返回
		"""
		#return '' % ()
		pass
		
	def update_data(self):
		"""
		根据tag信息更新data数据
		"""
		self.data = self.form_data()
	
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
		print self.format
		#for i in range(len(self.styles)):
			#self.styles[i].dump()
		for i in range(len(self.styles)):
			print self.styles[i].form_data()
			self.styles[i].dump()
		print ('=================== ASS Style Dump End ====================')

class AssEvents:
	"""
	AssEvent
	"""
	def __init__(self):
		self.events = []
		self.format = ''
		
	def parse(self, line):
		if line.startswith('Format:'):
			self.format= 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'
		#elif line.startswith('Dialogue:'):
		else:
			try:
				event = AssEntryDialogue(line, '[Events]')
			except UnknowDataError, err_msg:
				print UnknowDataError, ':', err_msg
			else:
				self.events.append(event)
			
	def dump(self):
		print ('================== ASS Event Dump Begin ===================')
		print '[Events]'
		print self.format
		#for i in range(len(self.events)):
			#self.events[i].dump()
		for i in range(len(self.events)):
			print self.events[i].form_data()
			self.events[i].dump()
		print ('=================== ASS Event Dump End ====================')
	
##class AssParseBase:
##	"""
##	ASS解析基类
##	实现基本的通用功能
##	"""
##	def __init__(self):
##		print ('AssParseBase init')
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
	
class AssParse(AssFile):
	"""
	Ass Pase Class
	"""
	def __init__(self, filename, encoding = 'utf-8', err_ignore = False):
		"""
		初始化here
		"""
		AssFile.__init__(self, filename, encoding)
		self.script_info = AssScriptInfo()
		self.styles = AssStyles()
		self.events = AssEvents()
		self.section = ''
		self.version = 0		#self.version     0: v4 style;  1: v4+ style;  2: v4++ style
		self.parse()
	
	def parse(self):
		"""
		解析
		"""
		for i in range(len(self.lines)):
			self.parse_line(self.lines[i])
		
	def parse_line(self, line):
		try:
			if line.lower() == '[script info]':
				self.section = '[Script Info]'
				
			elif line.lower() == '[v4 styles]':
				self.section = '[V4+ Styles]'
				self.version = 0
				
			elif line.lower() == '[v4+ styles]':
				self.section = '[V4+ Styles]'
				self.version = 1
				
			elif line.lower() == '[v4++ styles]':
				self.section = '[V4+ Styles]'
				self.version = 2
				
			elif line.lower() == '[events]':
				self.section = '[Events]'
				
			elif not self.section:
				raise UnknowDataError('Unknow Section: <%s>' % (line))
			
			else:
				if self.section == '[Script Info]':
					self.script_info.parse(line)
				elif self.section == '[V4+ Styles]':
					self.styles.parse(line, self.version)
				elif self.section == '[Events]':
					self.events.parse(line)
				else:
					raise UnknowDataError("Unkonw Data: <%s>" % (line))

		except UnknowDataError, err_msg:
			print UnknowDataError, ':', err_msg

if __name__ == "__main__" :
	# just for test

	filename = './l.ass'
	coding = 'utf-8'

	obj = AssParse(filename, coding)
	#obj.file_dump()
	obj.script_info.dump()
	obj.styles.dump()
	obj.events.dump()
	#obj.parse()
	#obj.dump()
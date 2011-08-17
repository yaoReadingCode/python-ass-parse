#!/usr/bin/env python
# coding: utf-8

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

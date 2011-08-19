#!/usr/bin/env python
# coding: utf-8



if __name__ == '__main__':

	from MediaInfoDLL import *
	
	MI = MediaInfoList()
	MI.Open('./1.mkk')
	
	print MI.Inform().encode('utf-8')
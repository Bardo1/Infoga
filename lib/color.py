#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
# infoga - Gathering Email Information Tool
# Coded by M0M0 (m4ll0k)

class colors:
	""" Colors """
	def __init__(self):
		self.BLUE = '\033[1;34m'
		self.GREEN = '\033[1;32m'
		self.RED = '\033[1;31m' 
		self.WHITE = '\033[1;37m'
		self.CYAN = '\033[1;36m'
		self.YELLOW = '\033[1;33m'
		self.RESET = '\033[0m'
		self.IND = '\033[04m'
		self.NWHITE = '\033[37m'

	def blue(self):
		return self.BLUE

	def green(self):
		return self.GREEN

	def red(self):
		return self.RED

	def white(self):
		return self.WHITE

	def cyan(self):
		return self.CYAN

	def yellow(self):
		return self.YELLOW

	def reset(self):
		return self.RESET

	def ind(self):
		return self.IND

	def nwhite(self):
		return self.NWHITE
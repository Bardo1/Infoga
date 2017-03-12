#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
# infoga - Gathering Email Information Tool
# Coded by M0M0 (m4ll0k)

import httplib
import re
import string 
import sys
from lib import color
from lib import parser

class yahoo_search:

	"""Yahoo Search Engine"""

	def __init__(self, keyword):

		self.keyword = keyword
		self.results = ""
		self.tresult = ""
		self.server = "search.yahoo.com"
		self.host = "search.yahoo.com"
		self.u_agent =  "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		self.t  = color.incolor.RESET  
		self.r  = color.incolor.RED
		self.y = color.incolor.YELLOW

	def run_search(self):

		try:
			con = httplib.HTTP(self.server)
			con.putrequest('GET', "/search?p=\"%40" +self.keyword+ "\"&b=500&pz=10")
			con.putheader('Host', self.host)
			con.putheader('User-agent', self.u_agent)
			con.endheaders()
			# return code,msg and header 
			returncode, returnmsg, headers = con.getreply()
			self.results = con.getfile().read()
			self.tresult += self.results
		except Exception as err:
			print "\t\t|"
			print "\t\t|__ {} Server not found!\n {}".format(self.r,self.t)

	def get_emails(self):

		_findemails = parser.inparser(self.tresult, self.keyword)
		return _findemails._emails()

	def process(self):
		
		self.run_search()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# infoga - Gathering Email Information Tool
# by M0M0 (m4ll0k) - (c) 2017


__license__ = """
Copyright (c) 2017, {M0M0 (m4ll0k)}
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of EnableSecurity or Trustwave nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from lib import color,parser, info 
from recon import *
##
try:
	import os
	import sys 
	import urllib3
	import requests
	import getopt
	import re
	import socket
	import json
	from urlparse import urlparse
	from time import strftime, sleep
except ImportError as error:
	print "\n{}[!] "+str(error)+"{}\n".format(color.incolor.RED,color.incolor.RESET)
##
##
class infoga:
	##
	def __init__(self, argv):
		self.argv = argv
		self.allemails = []
		self.conn = ""
		self.strf = "[%s] "% (strftime('%H:%M:%S'))
		# colors  
		self.r = color.incolor.RED
		self.y = color.incolor.YELLOW
		self.w = color.incolor.WHITE
		self.mw = color.incolor.MWHITE
		self.t = color.incolor.RESET 
		self.g = color.incolor.GREEN
		self.b = color.incolor.BLUE
		self.c = color.incolor.CRIMSON
		self.n = color.incolor.CYAN
		self.i = color.incolor.IND
		# info
		self.ver = info.__version__
		self.name = info.__name__
		self.desc = info.__info__
		self.code = info.__codename__
		self.auth = info.__author__
		self.url = info.__giturl__

	def banner(self):
		# ----------------------------------------------------------------
		print "{} ___        ___                    {}".format(self.r,self.t)
		print "{}|   .-----.'  _.-----.-----.---.-. {}".format(self.r,self.t)
		print "{}|.  |     |   _|  _  |  _  |  _  | {}".format(self.r,self.t)
		print "{}|.  |__|__|__| |_____|___  |___._| {}".format(self.r,self.t)
		print "{}|:  |                |_____|   {}{}\"{}\"{}".format(self.r,self.t,self.n,self.ver,self.t)
		print "{}|::.|{}{} N4m3:{} {}{} - {}{}        ".format(self.r,self.t,self.w,self.t,self.y,self.name,self.desc,self.t)
		print "{}|:..|{}{} C0d3n4m3:{} {}{}{}         ".format(self.r,self.t,self.w,self.t,self.y,self.code,self.t)
		print "{}|...|{}{} 4uth0r:{} {}{}{}           ".format(self.r,self.t,self.w,self.t,self.y,self.auth,self.t)    
		print "{}| - |{}{} Github:{} {}{}{}{}         ".format(self.r,self.t,self.w,self.t,self.i,self.y,self.url,self.t)
		print "{}`---'{}                            \n".format(self.r,self.t)

	def usage(self):
		# ------------------------------------------------------------------
		path = os.path.basename(sys.argv[0])
		self.banner()
		print "{}Usage: {} -t [target] -s [source]:{}\n".format(self.mw,path,self.t)
		print "{}\t-t\tDomain to search or company name{}".format(self.mw,self.t)
		print "{}\t-s\tData source: all, google, bing, pgp, yahoo{}".format(self.mw,self.t)
		print "{}\t-h\tShow this help and exit{}\n".format(self.mw,self.t)
		print "{}Examples:{}".format(self.mw,self.t)
		print "{}\t{} -t site.com -s all{}".format(self.mw,path,self.t)
		print "{}\t{} -t site.com -s [google, bing, pgp, yahoo]{}\n".format(self.mw,path,self.t)

	def google(self):
		print "{}{}{}{}Searching \"{}\" in Google...{}".format(self.mw,self.strf,self.t,self.y,self.keyword,self.t)
		search = googlesearch.google_search(self.keyword)
		search.process()
		self.allemails = search.get_emails()

	def bing(self):
		print "{}{}{}{}Searching \"{}\" in Bing...{}".format(self.mw,self.strf,self.t,self.y,self.keyword,self.t)
		search = bingsearch.bing_search(self.keyword)
		search.process()
		self.allemails = search.get_emails()

	def yahoo(self):
		print "{}{}{}{}Searching \"{}\" in Yahoo...{}".format(self.mw,self.strf,self.t,self.y,self.keyword,self.t)
		search = yahoosearch.yahoo_search(self.keyword)
		search.process()
		self.allemails = search.get_emails()

	def pgp(self):
		print "{}{}{}{}Searching \"{}\" in PGP...{}".format(self.mw,self.strf,self.t,self.y,self.keyword,self.t)
		search = pgpsearch.pgp_search(self.keyword)
		search.process()
		self.allemails = search.get_emails()

	def all(self):
		self.google()
		self.bing()
		self.yahoo()
		self.pgp()
		self.allemails.extend(self.allemails)
		self.allemails = sorted(set(self.allemails))

	def queque(self, findip):
		self.new = []
		for q in self.findip:
			if q not in self.new:
				self.new.append(q)
		return self.new
	def socket(self):
		v = '\n'.join(self.new)
		self.conn = socket.gethostbyaddr(v)
		return self.conn[0]

	def start(self):
		# ------------------------------------------------------------------
		if len(sys.argv) < 4:
			self.usage()
			sys.exit(0)
		try:
			opts,args = getopt.getopt(self.argv, "t:s:h")
		except getopt.GetoptError:
			self.usage()
			sys.exit(0)

		for opt,arg in opts:
			if opt == "-t":
				self.keyword = arg
			elif opt == "-h":
				self.usage()
				sys.exit(0)
			elif opt == "-s":
				self.engine = arg
				if self.engine not in ("all, google, bing, pgp, yahoo"):
					print "\n{}[!]{}{} Invalid search engine!! Try with: all, google, bing, yahoo or pgp.{}\n".format(self.r,self.t,self.w,self.t)
					sleep(1)
					self.usage()
					sys.exit(0)
				else:
					pass

		o = urlparse(self.keyword)
		if o[0] in ['http','https']:
			print "\n{}[!]{}{} Invalid scheme!! Try without: http://, https:// and www. :){}\n".format(self.r,self.t,self.w,self.t)
			sleep(1)
			sys.exit(0)
		else:
			pass

		###############################
		################################

		if self.engine == "google":
			self.banner()
			self.google()
			######################
		elif self.engine == "bing":
			self.banner()
			self.bing()
			######################
		elif self.engine == "yahoo":
			self.banner()
			self.yahoo()
			######################
		elif self.engine == "pgp":
			self.banner()
			self.pgp()
			######################
		elif self.engine == "all":
			self.banner()
			self.all()
			#######################
			#######################
		if self.allemails == []:
			print "\n{}{}{}{}Not found emails!!{}\n".format(self.mw,self.strf,self.t,self.r,self.t)
			sys.exit(0)
			##
		else:
			print "\n{}{}{}{}All Email Found: {}\n".format(self.mw,self.strf,self.t,self.y,self.t)
			for x in xrange(len(self.allemails)):
				data = {'lang':'en'}
				data['email'] = self.allemails[x]
				req = requests.post('http://www.mailtester.com/testmail.php', data=data)
				regex = re.compile(r"[0-9]+(?:\.[0-9]+){3}")
				self.findip = regex.findall(req.content)
				self.queque(self.findip)
				print "{}Email: {}{}".format(self.r,self.t,self.allemails[x])
				# ----
				for s in range(len(self.new)):
					net = urllib3.PoolManager()
					res = net.request('GET', "https://api.shodan.io/shodan/host/"+self.new[s]+\
						"?key=UNmOjxeFS2mPA3kmzm1sZwC0XjaTTksy")
					self.jso = json.loads(res.data)

				if 'country_code' and 'country_name' in self.jso:
					for c in range(len(self.new)):
						print "\t\t|_ {}{}{} ({})".format(self.g,self.new[s],self.t,self.socket())
						print "\t\t\t|"
						print "\t\t\t|__ Country: {}({}) - City: {} ({})".format(self.jso['country_code'],self.jso['country_name'],\
							self.jso['city'],self.jso['region_code'])
						print "\t\t\t|__ ASN: {} - ISP: {}".format(self.jso['asn'],self.jso['isp'])
						print "\t\t\t|__ Latitude: {} - Longitude: {}".format(self.jso['latitude'],self.jso['longitude'])
						print "\t\t\t|__ Hostname: {} - Organization: {}".format(self.jso['hostnames'],self.jso['org'])
						print ""

				elif 'No information available for that IP.' or 'error' in self.jso:
					print "\t\t\t|__ {} ({})"% (self.new[s],self.socket())
					print "\t\t\t|\t|__{}No information available for that IP!!{}".format(self.r,self.t)
					print ""
				
				else:
					print "\t\t\t|__ {} ({})".format(self.new[s],self.socket())

def main(argv):
	main = infoga(argv)
	main.start()

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt as err:
		print "\n{}[!] Ctrl+c.. :({}".format(color.incolor.RED,color.incolor.RESET)
		sleep(0.5)
		sys.exit(0)

		

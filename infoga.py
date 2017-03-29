#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
# infoga - Gathering Email Information Tool
# Coded by M0M0 (m4ll0k)

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

try:
	from lib import color
	from lib import parser
	from lib import info
	import os 
	import sys 
	import urllib3 
	import requests
	import re
	import socket
	import json
	import mechanize 
	import getopt
	from urlparse import urlparse
	from time import strftime, sleep
	from lxml.html import fromstring
	from recon import * 
except ImportError as err:
	print "%s]![%s %s%s%s"%("\033[1;31m","\033[0m","\033[1;38m",str(err),"\033[0m")
	sys.exit()


class Infoga:
	'''
	Infoga - Gathering Email Information Tool
	'''
	def __init__(self,argv):
		####### vars #######
		self.n = info.__name__
		self.i = info.__info__
		self.v = info.__version__
		self.c = info.__codename__
		self.a = info.__author__
		self.g = info.__giturl__
		self.s = info.__site__
		cc = color.colors()
		self.red = cc.red()
		self.green = cc.green()
		self.yellow = cc.yellow()
		self.white = cc.white()
		self.blue = cc.blue()
		self.cyan = cc.cyan()
		self.end = cc.reset()
		self.und = cc.ind()
		self.nwhite = cc.nwhite()
		self.argv = argv
		self.allemail = []
		self.new = []
		self.strf = "%s"%str((strftime('%H:%M:%S')))
		self.sock = []

	def banner(self):
		print self.red+"\t __        ___                      "+self.end
		print self.red+"\t|__.-----.'  _.-----.-----.---.-.   "+self.end
		print self.red+"\t|  |     |   _|  _  |  _  |  _  |   "+self.end
		print self.red+"\t|__|__|__|__| |_____|___  |___._|   "+self.end
		print self.red+"\t                    |_____|         "+self.end
		print self.yellow+"-- -=[%s %s%s %s - %s            %s"%(self.end,self.nwhite,self.n,self.v,self.i,self.end)
		print self.yellow+"-- -=[%s %s%s - \"%s\"           %s"%(self.end,self.nwhite,self.n,self.c,self.end)
		print self.yellow+"-- -=[%s %s%s - %s               %s"%(self.end,self.nwhite,self.a,self.s,self.end)
		print self.yellow+"-- -=[%s %s%s                  %s\n"%(self.end,self.nwhite,self.g,self.end)

	def usage(self):
		path = os.path.basename(sys.argv[0])
		self.banner()
		print "Usage: %s -t [target] -s [source]\n"% path
		print "\t-t\t\tDomain to search"
		print """\t-s\t\tData source: [all, google, yahoo, bing, \n\t\t\t\t\tpgp, yandex, baidu]"""
		print "\t-i\t\tGet email informations"
		print "\t--update\tUpdate tool"
		print "\t--version\tShow version"
		print "\t--help\t\tShow this help and exit\n"
		print "Examples:"
		print "\t %s -t http://www.site.com -s all"% path
		print "\t %s -t site.com -s [google, bing, ...]"% path
		print "\t %s -i email123@site.com"% path
		print ""
		sys.exit()

	def pprint(self,string,flag="+"):
		print '{}[{}]{}{}[{}]{} {}'.format(self.white,self.strf,self.end,self.green,str(flag),self.end,str(string))

	def nprint(self,string,flag="-"):
		print '{}[{}]{}{}[{}]{} {}'.format(self.white,self.strf,self.end,self.yellow,str(flag),self.end,str(string))
	
	def eprint(self,string,flag="!"):
		print '{}[{}]{}{}[{}]{} {}'.format(self.white,self.strf,self.end,self.red,str(flag),self.end,str(string))

	def google(self):
		self.pprint("Searching \"%s\" in Google..."%self.keyword)
		search = googlesearch.google_search(self.keyword)
		search.process()
		all_email = search.get_emails()
		self.allemail.extend(all_email)

	def bing(self):
		self.pprint("Searching \"%s\" in Bing..."%self.keyword)
		search = bingsearch.bing_search(self.keyword)
		search.process()
		all_email = search.get_emails()
		self.allemail.extend(all_email)

	def yahoo(self):
		self.pprint("Searching \"%s\" in Yahoo..."%self.keyword)
		search = yahoosearch.yahoo_search(self.keyword)
		search.process()
		all_email = search.get_emails()
		self.allemail.extend(all_email)

	def pgp(self):
		self.pprint("Searching \"%s\" in PGP..."%self.keyword)
		search = pgpsearch.pgp_search(self.keyword)
		search.process()
		all_email = search.get_emails()
		self.allemail.extend(all_email)

	def yandex(self):
		self.pprint("Searching \"%s\" in Yandex..."%self.keyword)
		search = yandexsearch.yandex_search(self.keyword)
		search.process()
		all_email = search.get_emails()
		self.allemail.extend(all_email)

	def baidu(self):
		self.pprint("Searching \"%s\" in Baidu..."%self.keyword)
		search = baidusearch.baidu_search(self.keyword)
		search.process()
		all_email = search.get_emails()
		self.allemail.extend(all_email)

	def all(self):
		self.google()
		self.bing()
		self.yahoo()
		self.pgp()
		self.yandex()
		self.baidu()
	
	def checkemail(self,email):
		email = self.email
		if '@' in email:
			allemail = str(email)
			data = {'lang':'en'}
			data['email'] = allemail
			req = requests.post('http://www.mailtester.com/testmail.php',data=data)
			pattern = re.compile(r'[0-9]+(?:\.[0-9]+){3}')
			findip = pattern.findall(req.content)
			for q in findip:
				if q not in self.new:
					self.new.append(q)
			tree = fromstring(req.text)
			tree.forms[0].getparent().remove(tree.forms[0])
			msg_list = tree.xpath('//table[last()]/tr[last()]/td[last()]/text()')
			msg = ' '.join([x.strip() for x in msg_list])
			
			if 'is valid' in msg:
				print ""
				self.pprint("{}Email:{} {}{}{} ({}{}{})".format(self.blue,self.end,self.yellow,allemail,self.end,self.green,msg,self.end))
			else:
				print ""
				self.pprint("{}Email:{} {}{}{} ({}{}{})".format(self.blue,self.end,self.yellow,allemail,self.end,self.red,msg,self.end))
			
			for s in range(len(self.new)):
				net = urllib3.PoolManager()
				res = net.request('GET',"https://api.shodan.io/shodan/host/"+self.new[s]+\
					"?key=UNmOjxeFS2mPA3kmzm1sZwC0XjaTTksy")
				self.jso = json.loads(res.data)

				if 'country_code' and 'country_name' in self.jso:
					print ""
					print "\t\t|_ {}{}{}".format(self.green,self.new[s],self.end)
					print "\t\t\t|"
					print "\t\t\t|__ Country: {}({}) - City: {} ({})".format(self.jso['country_code'],self.jso['country_name'],\
						self.jso['city'],self.jso['region_code'])
					print "\t\t\t|__ ASN: {} - ISP: {}".format(self.jso['asn'],self.jso['isp'])
					print "\t\t\t|__ Latitude: {} - Longitude: {}".format(self.jso['latitude'],self.jso['longitude'])
					print "\t\t\t|__ Hostname: {} - Organization: {}".format(self.jso['hostnames'],self.jso['org'])
					print ""

				elif 'No information available for that IP.' or 'error' in jso:
					print "\t\t|__ {}{}{}".format(self.green,self.new[s],self.end)
					print "\t\t\t|__{}No information available for that IP!!{}".format(self.red,self.end)
					print ""

				else:
					print "\t\t|__ {} ({})".format(str(self.new[s]))
			sys.exit()
		else:
			print ""
			self.eprint("{}Check your email... :){}".format(self.red,self.end))
			print ""
			sys.exit()

	def checkurl(self):
		o = urlparse(self.keyword)
		scheme = o.scheme
		netloc = o.netloc
		path = o.path

		if scheme not in ['http','https','']:
			print ""
			self.eprint("{}Scheme {} not supported!!{}".format(self.red,scheme,self.end))
			print ""
			sys.exit()

		if netloc == '':
			url = str(path)
		else:
			url = str(netloc)
		self.keyword = url

	def get_info(self):
		for x in xrange(len(self.allemail)):
			data = {'lang':'en'}
			data['email'] = self.allemail[x]
			req = requests.post('http://www.mailtester.com/testmail.php',data=data)
			pattern = re.compile(r'[0-9]+(?:\.[0-9]+){3}')
			findip = pattern.findall(req.content)
			for q in findip:
				if q not in self.new:
					self.new.append(q)

			self.pprint("{}Email:{} {}{}{}".format(self.blue,self.end,self.yellow,self.allemail[x],self.end))
			
			for s in range(len(self.new)):
				#########################
				net = urllib3.PoolManager()
				res = net.request('GET',"https://api.shodan.io/shodan/host/"+self.new[s]+\
					"?key=UNmOjxeFS2mPA3kmzm1sZwC0XjaTTksy")
				self.jso = json.loads(res.data,'utf-8')
				try:
					v = "\n".join(self.new)
					self.sock = socket.gethostbyaddr(v)
				except socket.herror:
					self.sock = ['%s'% self.jso['hostnames']]

				if 'country_code' and 'country_name' in self.jso:
					print "\t\t|_ {}{}{} ({})".format(self.green,self.new[s],self.end,self.sock[0])
					print "\t\t\t|"
					print "\t\t\t|__ Country: {}({}) - City: {} ({})".format(self.jso['country_code'],self.jso['country_name'],\
						self.jso['city'],self.jso['region_code'])
					print "\t\t\t|__ ASN: {} - ISP: {}".format(self.jso['asn'],self.jso['isp'])
					print "\t\t\t|__ Latitude: {} - Longitude: {}".format(self.jso['latitude'],self.jso['longitude'])
					print "\t\t\t|__ Hostname: {} - Organization: {}".format(self.jso['hostnames'],self.jso['org'])
					print ""

				elif 'No information available for that IP.' or 'error' in jso:
					print 
					print "\t\t|__ {}{}{} ({})".format(self.green,self.new[s],self.end,self.sock[0])
					print "\t\t\t|\t|__{}No information available for that IP!!{}".format(self.red,self.end)
					print ""

				else:
					print "\t\t|__ {} ({})".format(self.green,self.new[s],self.end,self.sock[0])

	def checkversion(self):
		print ""
		self.pprint("%s%s%s %s%s%s: %s%s%s"% (self.red,self.n,self.end,self.blue,self.v,self.end,self.white,self.i,self.end))
		print ""
		sys.exit(0)

	def checkupdate(self):
		path = os.getcwd()
		listpath = os.listdir(path)
		if ".git" not in listpath:
			print ""
			self.eprint("{}Git directory not found, please download Infoga from Github repository{}".format(self.red,self.end))
			print ""
			sys.exit()
		elif ".git" in listpath:
			print ""
			self.pprint("{}Updateting {}...{}".format(self.yellow,self.n,self.end))
			os.system('git pull')
			sys.exit()

	def start(self):
		if len(sys.argv) < 2:
			self.usage()
		try:
			opts,args = getopt.getopt(self.argv, "t:s:i:h:vu:",["update","version","help"])
		except getopt.GetoptError:
			self.usage()

		for opt,arg in opts:
			if opt == '-t':
				self.keyword = arg
				self.checkurl()
			elif opt == '-s':
				self.engine = arg
				if self.engine not in ("all","google","bing","yahoo","pgp","baidu","yandex"):
					print ""
					self.eprint("{}Invalid search engine!! Try with: all,google,bing,yahoo,pgp,baidu,yandex{}".format(self.red,self.end))
					print ""
					sys.exit()
			elif opt == '-i':
				self.email = arg
				self.checkemail(self.email)
			elif opt in ('-h','--help'):
				self.usage()
			elif opt in ('-v','--version'):
				self.checkversion()
			elif opt in ('-u','--update'):
				self.checkupdate()

		if self.engine == "google":
			self.banner()
			self.google()

		elif self.engine == "bing":
			self.banner()
			self.bing()

		elif self.engine == "yahoo":
			self.banner()
			self.yahoo()
		
		elif self.engine == "pgp":
			self.banner()
			self.pgp()

		elif self.engine == "yandex":
			self.banner()
			self.yandex()

		elif self.engine == "baidu":
			self.banner()
			self.baidu()

		elif self.engine == "all":
			self.banner()
			self.all()

		if self.allemail == []:
			self.nprint("Not found email!!\n")
			sys.exit()
		else:
			self.allemail = sorted(set(self.allemail))
			self.pprint("All email found: ")
			self.get_info()

def main(argv):
	main = Infoga(argv)
	main.start()

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt as err:
		print "{}Ctrl+c... Sn4duu :){}"%("\033[1;31m","\033[0m")
		sys.exit(0)


#coding="utf-8"

import urllib
import urllib2
import re
import codecs
import time

class QSBK:
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
		self.headers = {"User-Agent":self.user_agent}

	def getOnePage(self, pageIndex):
		try:
			url = "http://www.qiushibaike.com/hot/page/"+str(pageIndex)
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			content = response.read().decode("utf-8")
			return content
		except urllib2.URLError, e:
			if hasattr(e, "code"):
				print e.code
			elif hasattr(e, "reason"):
				print e.reason

	def getPageItems(self, pageIndex):
		content = self.getOnePage(pageIndex)
		if not content:
			print "page open fail!"
			return None
		else:
			print "page:", pageIndex
		pattern = re.compile('<a.*?title=.*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div class="content">'+
			'.*?<span>(.*?)</span>.*?</div>(.*?)<span class="stats-vote"><i class="number">(\d*?)</i>', re.S)
		items = re.findall(pattern, content)
		return items

	def saveItems(self, fp, items):
		for item in items:
			hasimg = re.search("img", item[2])
			if not hasimg and (int)(item[3]) >= 1000:
				fp.write(item[0]+"\n")
				fp.write(re.sub("<br/>", "\n", item[1])+"\n")
				fp.write(item[3]+"\n")

	def start(self):
		fp = codecs.open("qiubai.txt", "w", "utf-8")
		for self.pageIndex in range(1, 35):
			items = self.getPageItems(self.pageIndex)
			self.saveItems(fp, items)
		fp.close()

instance = QSBK()
instance.start()
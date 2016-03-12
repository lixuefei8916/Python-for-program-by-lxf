# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import urllib
import requests
import datetime

# website = 你要搜索的网站， 目仅支持 JD
website = 'www.jd.com'

# keyword_for_item = 你要搜索的商品， 例如 nike/vr眼睛 [注：每次只能输入1个， 还不支持列表]
keyword_for_item= '探路者 手杖'


# 搜索页面url的生成
class search_web_url(object):
	def __init__(self):
		self.__website = ''
		self.__keyword_for_item = ''
		self.__web_url = ''

	def set_website(self,website):
		self.__website = website

	def keyword_for_item(self,keyword_for_item):
		self.__keyword_for_item = urllib.quote(keyword_for_item) 
		# 如果keyword_for_item是中文，则转换为url编码 / 英文则忽略，需要urllib库.quote

	# 最终形成 某商品在某网站下的url  （自动判断JD，亚马逊，并生成url）
	def set_web_url(self):
		if self.__website == 'www.jd.com':
			self.__weburl = 'http://search.jd.com/Search?keyword=%s&enc=utf-8' %(self.__keyword_for_item)
			#print self.__weburl
			return self.__weburl

# url源码生成
class html(object):
	def __init__(self):
		self.__web_url = ''
		self.__keyword_for_item = ''

		self.__result_file = ''
		self.__html_file = ''

		self.__html_code = ''

	def set_web_message(self,weburl,keyword_for_item):
		self.__web_url = weburl
		self.__keyword_for_item = keyword_for_item

	def result_file(self):
		# 结果保存文件名： 日期+tiem.txt
		today = datetime.date.today()
		file_name = today.strftime("%Y%m%d")+ '-' + self.__keyword_for_item

		# html文件 存放的目录
		file_pwd = 'f:\\'

		#文件 绝对路径 + 文件名
		self.__result_file = file_pwd +  file_name + '.txt'
		#print self.__result_file

	def html_file(self):
		# web_pwd=网页存放目录
		html_file_pwd = 'f:\\'						

		# html文件名： 日期+tiem.html
		today = datetime.date.today()
		html_name = today.strftime("%Y%m%d")+ '-' + self.__keyword_for_item
		self.__html_file = html_file_pwd + html_name +'.html'								# web_name=网页文件名
		#print self.__html_file

	def html_code(self):
		conn = requests.get(self.__web_url)
		conn.url
		self.__html_code = conn.text
		return self.__html_code

	def download_html_file(self):
		reload(sys)							# 规定编码，无此行会报告
		sys.setdefaultencoding( "utf-8" )	# UnicodeEncodeError: 'ascii' codec can't encode characters
		f = file(self.__html_file,'w') 		# 要写的文件 和 赋予写权限
		f.write(self.__html_code)			# 写什么内容
		f.close								# 正常关闭文件
		# 注意，如果是中文， 这里的文件名是有问题的， 怎么转换成中文？

class spider_engine(object):
	def __init__(self):
		self.__price_list = ''
		self.__html_code = ''
		self.__items_name_list = []

	def set_(self,html_code):
		self.__html_code = html_code

	def price_list(self):
		#先提取出 </em><i>199.00<
		pattern1 = re.compile(r'</em><i>\d+.\d+\<')
		x = pattern1.findall(self.__html_code)
		price_code = str(x)
		# 再提取出价格
		pattern2 = re.compile(r'\d+.\d+')
		y = pattern2.findall(price_code)
		self.__price_list = y
		#print self.__price_list

	def items_name_list(self):
		# 名称
		# <a target="_blank" title="暴风魔镜4代 黄金版 金版" href="//item.jd.com/10057427339.html"
		reload(sys)							# 规定编码，无此行会报告
		sys.setdefaultencoding( "utf-8" )	# UnicodeEncodeError: 'ascii' codec can't encode characters
		zh_pattern = self.__html_code.decode('utf8') # 以上3行是一组，不可分开，否则 encode报错
		#pattern3 = re.compile(u'[\u4e00-\u9fa5]+') 
		#pattern3 = re.compile(r'<a target="_blank" title=".+') 
		#pattern3 = re.compile(u'title="[\u4e00-\u9fa5]+.+"\s\href')    【OK ，但有纰漏，例如前两行】
		#pattern3 = re.compile(u'title="[\u4e00-\u9fa5]+\s[\u4e00-\u9fa5]+.+"\s\href')  【完全正确的方式，干净、完整】

		# 【OK 勿改】pattern3 = re.compile(u'title=".+\s[\u4e00-\u9fa5]+.+"\s\href') 
		pattern3 = re.compile(u'<a target="_blank" title=".+"\s\href')   
		x = pattern3.findall(zh_pattern)

		for i in x:
			pattern4 = re.compile(u'e=".+"')
			y = pattern4.findall(i)
			for t in y:
				tmp = t.decode('utf-8')
				#print tmp
				self.__items_name_list.append(tmp)
		#print self.__items_name_list
		'''
			#简单 - 打印出中文
			for i in x:
				tmp = i.decode('utf-8')
				print tmp

			#难 - 下面把 tile="xxxxxxxxxxxx" herf 正则掉
			for i in x:
				pattern4 = re.compile(u'[\u4e00-\u9fa5]+.+"')
				y = pattern4.findall(i)
				for t in y:
					tmp = t.decode('utf-8')
					print tmp
		'''
	def result_list(self):
		price_tables = dict(map(lambda x,y:[x,y], self.__items_name_list,self.__price_list))
		tmp = json.dumps(price_tables,encoding='UTF-8', ensure_ascii=False)

		today = datetime.date.today()
		time = today.strftime("%Y%m%d")

		for key,value in price_tables.items():
			print '========================'
			print 'name=',key , '\n' 'price=',value	, '\n' 'time=',time	

# ===============================================================================================================================


# 生成url链接，需要站点和要搜索的关键字
lxf_engine = search_web_url()
lxf_engine.set_website(website)
lxf_engine.keyword_for_item(keyword_for_item)
weburl = lxf_engine.set_web_url()


# html相关，，下载url源码
lxf_engine = html()
lxf_engine.set_web_message(weburl,keyword_for_item)
#lxf_engine.result_file()
#lxf_engine.html_file()
#lxf_engine.download_html_file()
html_code = lxf_engine.html_code()


# 爬虫主程序：正则，打印结果
lxf_engine = spider_engine()
lxf_engine.set_(html_code)
lxf_engine.price_list()
lxf_engine.items_name_list()
lxf_engine.result_list()

# ===============================================================================================================================



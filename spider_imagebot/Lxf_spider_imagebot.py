# -*- coding: utf-8 -*-
#【6】# web爬虫 - 抓图【class版】
# 访问 国家地理网站抓取上面的图片，并且图片文件名与html源码中的名一致
import os
import re
import sys
import requests
# ----------------------------------------------------
web_url = r'http://www.nationalgeographic.com.cn/'	# web_url=网页地址
html_pwd = r'/home/lxf/'							# web_pwd=网页存放目录
html_name = '1.html'								# web_name=网页文件名
pic_pwd = r'/home/lxf/'								# pic_pwd = 图片存放路径
# pic_url=图片地址 [变量，待re正则出结果]
# pic_name = 图片文件名	 [变量，待re正则出结果]
# ----------------------------------------------------
class Lxf_spider_imagebot(object):
	def __init__(self):
		self.__weburl = 'blank'
		self.__html_code = 'blank'
		self.__pic_url_list = 'blank'

		self.__html_pwd = 'blank'
		self.__html_name = 'blank' 
		self.__html_file = self.__html_pwd + self.__html_name

		self.__pic_pwd = 'blank'


	# 设置网页url地址
	def set_weburl(self,x):					# 设置 url地址， 这是私有的
		self.__weburl = x

	def set_html_file(self,x,y):
		self.__html_pwd = x
		self.__html_name = y

	def set_pic_file(self,x):
		self.__pic_pwd = x

	# 打印url地址
	#def print_weburl(self):
		#print self.__weburl

	def requests_weburl(self):				# requests 网页地址
		conn = requests.get(self.__weburl)
		conn.url
		html_code = conn.text
		self.__html_code = html_code 		# 将结果传入 self.__html_code

	def download_htmlcode(self):			# 下载html源码到本地
		reload(sys)							# 规定编码，无此行会报告
		sys.setdefaultencoding( "utf-8" )	# UnicodeEncodeError: 'ascii' codec can't encode characters
		f = file(self.__html_file,'w') 		# 要写的文件 和 赋予写权限
		f.write(self.__html_code)			# 写什么内容
		f.close								# 正常关闭文件

	def search_pic_url(self):
		pattern = re.compile(r'http://\S+\.\jpg|http://\S+\.\png')
		x = pattern.findall(self.__html_code)
		self.__pic_url_list = x

			#解释： (1) \ 是 and 的意思
			#		(2) http://开始，
			#		(3) . 
			#		(4)S是匹配“非空”字符,+是任意数量 
			#		(5). 
			#		(6)com
			#		(7) A|B  意思是 A和B都被检索出来 

	def download_pic(self):
		for pic_url in self.__pic_url_list:
			conn = requests.get(pic_url)
			pattern = re.compile(r'\w+.\jpg$|\w+.\jpg$')
				# 【提取源码中图片的文件名】
    			# 预期提取图片文件名例：20151116031138474.jpg
    			# w+ 代表非字符单属于单词和数字的
    			# $ 代表从尾部匹配
			pic_name = pattern.search(pic_url)
			if pic_name:
				name = pic_name.group()
				pic_file = self.__pic_pwd + name 		# 图片保存目录 + 文件名
				with open(str(pic_file),'wb') as lxf:   #下载图片，wb是写权限
					lxf.write(conn.content)				#执行下载图片（写图片文件）

if __name__ == '__main__': 
	lxf = Lxf_spider_imagebot() 

	lxf.set_weburl(web_url) 							# 设置:访问 url
	lxf.set_html_file(html_pwd,html_name)				# 设置：html源码存放的本地目录
	lxf.set_pic_file(pic_pwd)
	#lxf.print_weburl()
	lxf.requests_weburl() 								# requests 网页地址
	#lxf.download_htmlcode()							# 下载 html到本地
	lxf.search_pic_url()
	lxf.download_pic()


# -*- coding: utf-8 -*-


import os
import re
import sys
import json
import requests
import datetime

web_url = r'http://search.jd.com/Search?keyword=vr%E7%9C%BC%E9%95%9C&enc=utf-8&wq=vr%E7%9C%BC%E9%95%9C&pvid=0t29t4li.olsn1k'	# web_url=网页地址


today = datetime.date.today()
file_name = today.strftime("%Y%m%d")
file_pwd = '/home/lxf/price/'
file_ = file_pwd + file_name + '.txt'
print file_

html_pwd = r'/home/lxf/jd-vr/'						# web_pwd=网页存放目录
html_name = today.strftime("%Y%m%d")
html_file = html_pwd + file_name +'.html'								# web_name=网页文件名
print html_file


conn = requests.get(web_url)
conn.url
html_code = conn.text


reload(sys)							# 规定编码，无此行会报告
sys.setdefaultencoding( "utf-8" )	# UnicodeEncodeError: 'ascii' codec can't encode characters
f = file(html_file,'w') 		# 要写的文件 和 赋予写权限
f.write(html_code)			# 写什么内容
f.close								# 正常关闭文件


# ======================================================================
# 价格
#先提取出 </em><i>199.00<
pattern1 = re.compile(r'</em><i>\d+.\d+\<')
x = pattern1.findall(html_code)
price_code = str(x)
# 再提取出价格
pattern2 = re.compile(r'\d+.\d+')
y = pattern2.findall(price_code)
price_list = y


# ======================================================================
# 名称
# <a target="_blank" title="暴风魔镜4代 黄金版 金版" href="//item.jd.com/10057427339.html"

zh_pattern = html_code.decode('utf8')
#pattern3 = re.compile(u'[\u4e00-\u9fa5]+')
#pattern3 = re.compile(r'<a target="_blank" title=".+') 
#pattern3 = re.compile(u'title="[\u4e00-\u9fa5]+.+"\s\href')    【OK ，但有纰漏，例如前两行】
#pattern3 = re.compile(u'title="[\u4e00-\u9fa5]+\s[\u4e00-\u9fa5]+.+"\s\href')  【完全正确的方式，干净、完整】

pattern3 = re.compile(u'title="[\u4e00-\u9fa5]+\s[\u4e00-\u9fa5]+.+"\s\href')  
x = pattern3.findall(zh_pattern)

name_list = []

for i in x:
	pattern4 = re.compile(u'[\u4e00-\u9fa5]+.+"')
	y = pattern4.findall(i)
	for t in y:
		tmp = t.decode('utf-8')
		#print tmp
		name_list.append(tmp)


'''
#简单 - 打印出中文
for i in x:
	tmp = i.decode('utf-8')
	print tmp
'''

'''
#难 - 下面把 tile="xxxxxxxxxxxx" herf 正则掉
for i in x:
	pattern4 = re.compile(u'[\u4e00-\u9fa5]+.+"')
	y = pattern4.findall(i)
	for t in y:
		tmp = t.decode('utf-8')
		print tmp
'''



# ======================================================================


# name_list 和 price_list 合并成字典
price_tables = dict(map(lambda x,y:[x,y], name_list,price_list))
tmp = json.dumps(price_tables,encoding='UTF-8', ensure_ascii=False)

for key,value in price_tables.items():
	print '========================'
	print 'name=',key , '\n' 'price=',value

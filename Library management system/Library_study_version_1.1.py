#-*- coding: utf-8 -*-
#u'3个对象 ； 1)父类=图书馆(图书列表、查询书籍是否存在-->查询是否被订阅--> Guest订阅) 
#u'           2)Admin（加、删书籍）  3)Guest（借阅书籍）'

class Library(object):
	def __init__(self):
		self.book_list = {'math':'lxf','chinese':'Tom','english':'free'}

	def print_book_list(self):					#打印我图书馆全部图书
		return self.book_list

	def search_book(self,book_name):			#查找图书
		if book_name in self.book_list:
			print '图书馆中有这本书籍'
			print '是否借阅这本书?'
			tmp = Library_Guest()
			return tmp.borrow_book(book_name)
		else:
			print "对不起，图书馆中没有这本书"

class Library_Admin(Library):
	def add_book(self,book_name):				#Admin 添加书籍
		self.book_list[book_name]='free'
		return self.book_list

	def del_book(self,book_name):				#Admin 删除书籍
		self.book_list.pop(book_name)

class Library_Guest(Library):					#Guest 查询目标书籍是否被借阅
	def borrow_book(self,book_name):
		tmp = self.book_list[book_name]
		if tmp is not 'free':
			print '对不起！！ 这本书已被借阅'
		else:
			people = raw_input('Please enter you name: ')     # 订阅目标书籍
			self.book_list[book_name] = people
			return self.book_list

lxf = Library_Admin()
lxf.add_book('python')
guest = Library_Guest()
guest.borrow_book('math')
guest.borrow_book('english')
lxf = Library()
lxf.search_book('english')

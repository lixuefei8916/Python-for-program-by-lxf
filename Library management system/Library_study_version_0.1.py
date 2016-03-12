class Library(object):

	def __init__(self):
		self.book_list = ['math','chinese','english','Politics']
		self.reservation_record = {'chinese':'Obama','math':'lxf','english':'free','politics':'free'}

	def print_all_book_list(self):
		print self.book_list

	def book_add(self,book_name):
		self.book_list.append(book_name)
		self.reservation_record[book_name] = 'free'
		print self.reservation_record

	def book_del(self,book_name):
		print type(book_name)
		print type(self.book_list)     # just check list or tunple
		self.book_list.pop(book_name)

	def search_book(self,book_name):
		if book_name in self.book_list:
			print "We have this book"
			return self.who_booked_this_book(book_name)
		else:
			print "Sorry Sir! We don't have this one"

	def who_booked_this_book(self,book_name):
		people = self.reservation_record[book_name]
		if people is not 'free':
			print "Sorry,This book has been [%s] reservation" %(people)
		else:
			print "You can book this one,Do you want Book it?"
			people_name = raw_input("Please enter you Name: ")
			return self.booked_the_book(book_name,people_name)

	def booked_the_book(self,book_name,people_name):
		self.reservation_record[book_name]=people_name
		print self.reservation_record

lxf = Library()
lxf.book_add('history')
lxf.book_del('history')    # it has a problem"TypeError: an integer is required"
lxf.print_all_book_list()
lxf.search_book('The kite runner')
lxf.search_book('chinese')
lxf.search_book('english')



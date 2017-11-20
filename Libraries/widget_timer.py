import json
import cgi
import localization

class WidgetTimer:
	def __init__(self):
		self.__datatable = None
		self.__timer_list = None

	def set_data(self, data):
		timer = []
		for t in data:
			timer.append({"id" : t.id,
					"Picture" : "<img src='/e574b9ce-9582-4962-ad7b-b11820dacc3d.png' />",
					"Name" : "<h1>" + t.name + "</h1><p class='clearfix'></p><p>" + get_period(t.period.split(":")) + "</p><p></p>",
					"Edit" : "<a href=''><img src='/bfd88533-b697-4ce2-8a4f-ba85e269820b.res'/>Edit timer</a>",
					"Delete" : "<a href=''>Delete</a>"})

		self.__timer_list = json.dumps(timer)

	def render(self, datatable):
		self.__datatable = datatable
		self.__datatable.data = self.__timer_list

def get_period(period):
	period_str = "once "
	if len(period) == 4:
		if int(period[0]) > 1 :
			period_str += str(int(period[0])) + " days "
		elif int(period[0]) ==  1 :
			period_str += str(int(period[0]))  + " day "
		if int(period[1]) > 1 :
			period_str += str(int(period[1])) + " hours "
		elif int(period[1]) ==  1 :
			period_str += str(int(period[1])) + " hour "
		if int(period[2]) > 1 :
			period_str += str(int(period[2])) + " mins "
		elif int(period[2]) ==  1 :
			period_str += str(int(period[2])) + " min "
		if int(period[3]) > 1 :
			period_str += str(int(period[3])) + " secs "
		elif int(period[3]) ==  1 :
			period_str += str(int(period[3])) + " sec "
	if len(period) == 3:
		if int(period[1]) > 1 :
			period_str += str(int(period[1])) + " hours "
		elif int(period[1]) ==  1 :
			period_str += str(int(period[1])) + " hour "
		if int(period[2]) > 1 :
			period_str += str(int(period[2])) + " mins "
		elif int(period[2]) ==  1 :
			period_str += str(int(period[2])) + " min "
		if int(period[3]) > 1 :
			period_str += str(int(period[3])) + " secs "
		elif int(period[3]) ==  1 :
			period_str += str(int(period[3])) + " sec "
	if len(period) == 2:
		if int(period[2]) > 1 :
			period_str += str(int(period[2])) + " mins "
		elif int(period[2]) ==  1 :
			period_str += str(int(period[2])) + " min "
		if int(period[3]) > 1 :
			period_str += str(int(period[3])) + " secs "
		elif int(period[3]) ==  1 :
			period_str += str(int(period[3])) + " sec "
	if len(period) == 1:
		if int(period[3]) > 1 :
			period_str += str(int(period[3])) + " secs "
		elif int(period[3]) ==  1 :
			period_str += istr(int(period[3])) + " sec "

	return period_str

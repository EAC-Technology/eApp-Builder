import ProAdmin
import json
import localization

class WidgetProAdminUsers:

	def __init__( self ):

		self.__datatabe 	= None
		self.__page = 0
		self.users = ProAdmin.application().get_users()
		self.__per_page				= 10

	def set_page(self,page):
		self.__page = page - 1

	def render( self, datatable, pager = None):
		lang = localization.get_lang()

		pages_count = 0
		data 		= []
		objects = self.users

		count 	= len( objects ) 										# users count
		left 	= self.__page * self.__per_page										# from 	- index
		right 	= left + self.__per_page if left + self.__per_page <= count else count			# to 	- index
		pages_count = 	str( count/self.__per_page + 1 )\
						if count % self.__per_page > 0 	\
						else str( count/ self.__per_page )# number of pages

		datatable.header = json.dumps([u"guid", lang["account_column"], lang["name_column"], lang["login_column"]])
		for obj in objects[left:right]:
			data.append([obj.guid, obj.name, obj.email, "<a href='/proadmin_users?guid=" + obj.guid + "'><img src='/84015a56-0487-4bfc-8a6c-2fc810df1dfa.res' /></a>"])

		datatable.data 		= json.dumps(data)

		if data:
			pager.pagescount 	= pages_count
			pager.currentpage 	= self.__page+1
			pager.top = str( 237  + 38 * len(data ) + 100 )
			datatable.visible   = pager.visible = "1"
		else:
			pager.action( "hide", [ "" ] )




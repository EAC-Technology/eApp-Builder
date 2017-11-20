country_list_str = u'{"0": "Argentina", "1": "Australia", "2": "Bangladesh", "3": "Belgie", "4": "Belgique", "5": "Brasil", "6": "\u0411\u044a\u043b\u0433\u0430\u0440\u0438\u044f", "7": "Burma", "8": "Cambodia", "9": "Canada", "10": "Ceska Republika", "11": "Chile", "12": "Colombia", "13": "Costa Rica", "14": "Deutschland", "15": "Espana", "16": "France", "17": "Hong Kong", "18": "India", "19": "Indonesia", "20": "Ireland", "21": "Jamaica", "22": "Laos", "23": "Macau", "24": "Mexico", "25": "Malaysia", "26": "Mongolia", "27": "Nederland", "28": "Nepal", "29": "Panama", "30": "Peru", "31": "Philippines", "32": "Polska", "33": "Puerto Rico", "34": "Republica Dominicana", "35": "Romania", "36": "\u0420\u043e\u0441\u0441\u0438\u044f", "37": "Singapore", "38": "South Africa", "39": "Sri Lanka", "40": "Turkiye", "41": "Taiwan", "42": "Trinidad and Tobago", "43": "\u0423\u043a\u0440\u0430\u0457\u043d\u0430", "44": "United Kingdom", "45": "United States of America", "46": "Uruguay", "47": "Venezuela", "48": "Vietnam", "-1":""}'

country_list = [ u"Argentina",u"Bangladesh",u"Australia",u"Belgie",u"Belgique",\
u"Brasil",u"България",u"Burma",u"Cambodia",u"Canada",u"Ceska Republika",u"Chile",\
u"Colombia",u"Costa Rica",u"Deutschland",u"Espana",u"France",u"Hong Kong",u"India",\
u"Indonesia",u"Ireland",u"Jamaica",u"Laos",u"Macau",u"Mexico",u"Malaysia",u"Mongolia",\
u"Nederland",u"Nepal",u"Panama",u"Peru",u"Philippines",u"Polska",u"Puerto Rico",\
u"Republica Dominicana",u"Romania",u"Россия",u"Singapore",u"South Africa",u"Sri Lanka",\
u"Turkiye",u"Taiwan",u"Trinidad and Tobago",u"Україна",u"United Kingdom",\
u"United States of America",u"Uruguay",u"Venezuela",u"Vietnam"]



#from collections import OrderedDict
#from json import dumps
#d = OrderedDict()
#i=0
#for k in country_list:
#	d[i] = k
#	i+=1
#raise Exception( dumps(d) )


login_page_url 			= "/login"
home_page_url  			= "/"
proadmin_attention_url 	= "/proadmin_attention"
license_url 			= "/license"



vdom_container = None
def redirect( url ):
	if vdom_container:
		vdom_container.action( "goTo", [ url ] )
	else:
		response.redirect( url )



import ProAdmin
def authenticated( method ):
	def wrapper( *args, **kwargs ):
		if ProAdmin.current_user() is None:
			redirect( login_page_url )
		else:
			return method()
	return wrapper


def administrator( method ):
	def wrapper( *args, **kwargs ):
		current_user = ProAdmin.current_user()
		if bool( ProAdmin.application().rules( subject = current_user, access='a' ) ):
			return method()
		else:
			redirect( home_page_url )
	return wrapper


def local_scheme( method ):
	def wrapper( *args, **kwargs ):
		if ProAdmin.scheme().is_remote():
			redirect( proadmin_attention_url )
		else:
			return method()
	return wrapper

def license_confirmed( method ):
	def wrapper( *args, **kwargs ):
		from class_license import License
		if not License().confirmed:
			redirect( license_url )
		else:
			return method()
	return wrapper


from engine.exceptions import RenderTermination
def error_handler( method ):
	def wrapper( *args, **kwargs ):
		try:
			return method()
		except RenderTermination:
			raise
		except Exception, ex:
			raise
			session[ "error" ] = unicode(ex)
			redirect( home_page_url )
	return wrapper

def active_directory_scheme( method ):
	def wrapper( *args, **kwargs ):
		 if ProAdmin.scheme().type == "active_directory":
		 	return method()
	return wrapper

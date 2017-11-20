import localization_ru
import localization_fr
import localization_en
import localization_bg

def _get_lang( not_user = None ):
	#return localization_bg
	if session.get( "lang" ) is None:
		if "HTTP_ACCEPT-LANGUAGE" in request.environment:
			set_lang = str(request.environment["HTTP_ACCEPT-LANGUAGE"])[:2]
			switch_lang(set_lang)

	if session["lang"] == "ru":		return localization_ru
	elif session["lang"] == "fr":	return localization_fr
	elif session["lang"] == "bg":	return localization_bg
	else:							return localization_en

def get_lang(not_used = None):
	return _get_lang( not_used ).localization_dict

def get_lang_rectangle( not_used = None ):
	return _get_lang( not_used ).lang_rectangle

def switch_lang( newlang ):
	session["lang"] = newlang

def current_language():
	return session["lang"]



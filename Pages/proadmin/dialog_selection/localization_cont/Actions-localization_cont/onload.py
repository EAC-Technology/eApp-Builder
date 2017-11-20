import localization


if  "ln" in request.arguments:
 lang = request.arguments.get("ln")
 localization.switch_lang(lang )
 response.cookies["language"] = lang
 response.cookies["language"]["max-age"]= str(60*60*24*365)
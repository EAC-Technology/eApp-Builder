from AppinmailSSO import AppinmailSSO

if 'VDOM_REST_API_CERT' in session:
	del session['VDOM_REST_API_CERT']

if not AppinmailSSO.current_user():
	AppinmailSSO.authorize('https://admin.appinmail.io')

if AppinmailSSO.access_token():
	session['access_token'] = AppinmailSSO.access_token()
	response.write('ok')

response.write('failed')

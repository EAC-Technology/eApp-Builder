import ProAdmin

try:
    user = ProAdmin.current_user()
    if user:
        response.redirect( '/main' )
    else:
        response.redirect( '/login' )

except:
    from vdom_trace import Trace
    response.write('<pre>' + Trace.exception_trace() + '</pre>')

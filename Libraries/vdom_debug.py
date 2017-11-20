import sys, traceback
import cProfile, StringIO, pstats

from datetime import datetime, timedelta


def _pre(*args):
	args = map(str, args)
	text = ' '.join(args)
	text = text.replace('<', '&lt;').replace('>', '&gt;')
	return '<pre style="white-space: pre-wrap;">\n{0}\n</pre>'.format(text)

def p(*args, **kwargs):
	s = _pre(*args)
	response.write(s, kwargs.get('cont'))

def r(*args):
	s = _pre(*args)
	raise Exception(s)

def d(x):
	p(dir(x))

def t(x):
	p(type(x))

def l(x):
	p(len(x))



def profile(func, *args, **kwargs):
	profile = cProfile.Profile()
	profile.runcall(func, *args, **kwargs)

	res = StringIO.StringIO()
	ps = pstats.Stats(profile, stream=res).sort_stats('cumulative')
	ps.print_stats()

	return res.getvalue()

def p_ex():
	p(exception_trace())

def exception_trace():
	_type, val, tb = sys.exc_info()
	s = '\n'.join(traceback.format_exception( _type, val, tb ))
	return s

def ex():
	return exception_trace()


def counts_per_second(func):
	count = 0
	t = datetime.now() + timedelta(seconds=5)
	while datetime.now() < t:
		func()
		count += 1
	return count / 5.0


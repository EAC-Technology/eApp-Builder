
import datetime

class VEE_timer(object):
	def __init__(self, name, delay, hash_value ):
		"""delay should be in format 00:00:00:00, where each digit - delay in day:hr:min:sec"""
		self.delay = map(int,delay.split(':'))
		self.name = name
		self.active = True
		self.hash_value = hash_value
		self.last_run = datetime.datetime.now()
		if not len(self.delay) == 4:
			raise Exception ("Timer delay have invalid format")

	def check(self):
		"""Return true if since last run needed time already passed. Timer should be active"""
		if self.active and self.last_run + datetime.timedelta(days = self.delay[0],
				hours=self.delay[1],minutes=self.delay[2], seconds = self.delay[3])<=datetime.datetime.now():
			self.last_run = datetime.datetime.now()
			return True

import json

try:
	import ProAdmin
	ProAdmin.sync()
	session["response"] = json.dumps(["success"])
except:
	session["response"] = json.dumps(["error", "Synchronization failed"])

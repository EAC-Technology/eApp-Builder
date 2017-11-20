from api_helper import *
from models import Workspace
import json


#@license_confirmed
@authenticated
@error_handler
@parse_json
def main( data ):

	workspaces_json = { "workspaces": [w.to_json() for w in Workspace.all()] }
	write_response( workspaces_json )

main()

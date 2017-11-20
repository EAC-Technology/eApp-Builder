try:
	VDOM_CONFIG["RENDER-TIMEOUT"] = 300
	from db_update import Update
	current_version = Update().get_current_version()
	updated_version = Update().update()
	self.output.value = "Update has been successfully completed. Version before update call: {0}. Version after update call: {1}.".format( current_version, updated_version )

except Exception, ex:
	self.output.value = "ERRROR: {0}".format( ex.message )

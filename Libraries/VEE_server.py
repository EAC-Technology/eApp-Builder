from vscript.wrappers.environment import v_server



vscript_wrappers_name="wrappers"



class v_server_wrapper( object ):

	def __init__( self ):
		self.server = v_server()


	def v_application( self ):
		return self.server.v_application()


	def v_sendmail( self, *args, **kwargs ):
		return self.server.v_sendmail( *args, **kwargs )


	def v_mailstatus( self, *args, **kwargs ):
		return self.server.v_mailstatus( *args, **kwargs )


	def v_mailer( self, *args, **kwargs ):
		return self.server.v_mailer( *args, **kwargs )


environment =  (
	(	"v_mailserverclosedconnection"		, vscript_wrappers_name ),
	(	"v_mailservernomessageindex"		, vscript_wrappers_name ),
	(	"v_mailservererror"					, vscript_wrappers_name ),
	(	"v_mailserveralreadyconnectederror"	, vscript_wrappers_name ),
	(   "v_server"							, v_server_wrapper()	),
	(   "v_attachment"						, vscript_wrappers_name ),
	(   "v_mailattachment"					, vscript_wrappers_name ),
	(   "v_message"							, vscript_wrappers_name ),
	(   "v_mailmessage"						, vscript_wrappers_name ),
    (   "v_smtpsettings"					, vscript_wrappers_name ),
)

#16.01.2013
#clean and improve library

#23.01.2013
#modify v_timer

#30.01.2013
#move code to other library

from datetime import datetime
from class_db import Database
from cgi import escape
from hashlib import md5
from VEE_utils import   AutoCast, CachedProperty, is_dict,\
                        v_PropertySimple, v_PropertyComplex, \
                        v_PropertyReadOnly, encodeUTF8, decodeUTF8, \
                        AutoCastCachedProperty

from vscript.subtypes import  binary, generic
from vscript import errors, error
import base64, cStringIO, re



property_pattern = re.compile( "^(v_*)" )



class v_BaseException( errors.generic ):

    def __init__( self, message ):
        errors.generic.__init__( self, message =  message )

class v_BadObjectType( v_BaseException ):
    pass



class base_object( generic ):

    def __init__( self, object = None ):
        generic.__init__( self )
        self.object  = object


    @AutoCast
    def __getattr__( self, key ):
        return getattr( self.object, property_pattern.sub( "", key ) )


    def __nonzero__( self ):
        return True



@AutoCast
def v_generateguid( ):
    from uuid import uuid4
    return str( uuid4() )



class v_xmldialog( object ):

    def __init__( self ):
        self.xml            = None
        self.arguments      = {}
        self.macros_id      = None
        self.width          = "400"
        self.height         = "300"
        self.container_guid = ""
        self.visible        = False
        self.actions        = []


    @AutoCast
    @v_PropertySimple
    def v_visible( self, value, retVal ):
        if retVal: return self.visible
        else: self.visible = value


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_macrosid( self ):
        return self.macros_id


    @AutoCast
    def v_setsize( self, width, height ):
        self.width = width
        self.height = height


    @AutoCast
    def v_show( self, xml_data ):
        self.xml = xml_data


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_containerguid( self ):
        return self.container_guid


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_arguments( self ):
        return self.arguments

    @AutoCast
    def v_executecallback(self, callback, data):
        self.actions.append([callback, data])

    @AutoCast
    def v_uploadedfile(self, guid):
        f = request.uploaded_file(guid)
        return v_uploadedfileobj(f) if f else None

    @AutoCast
    def v_clearfiles(self):
        request.clear_files()

    #obsolete methods names
    v_get_macros_id = v_macrosid
    v_set_size = v_setsize
    v_show_xml_form = v_show
    v_obj_guid = v_containerguid
    v_get_answer = v_arguments


class v_uploadedfileobj(generic):

    def __init__(self, file):
        self.file = file

    @AutoCast
    @v_PropertyReadOnly
    def v_data(self):
        f = self.file.handler
        f.seek(0)
        value = f.read()
        f.seek(0)
        return binary(value)

    @AutoCast
    @v_PropertyReadOnly
    def v_name(self):
        return self.file.name

    @AutoCast
    def v_remove(self):
        return self.file.remove()


class v_dynamicvdom( object ):

    def __init__( self, dynobj ):
        self.vdomdynobj     = dynobj

    @AutoCast
    def v_render(self, vdomxml, vdomactions="", absolute=False):
        self.vdomdynobj.vdomxml = vdomxml
        self.vdomdynobj.vdomactions = vdomactions
        return self.vdomdynobj.render(None, raw_content=absolute)

    @AutoCast
    @v_PropertySimple
    def v_top( self, value, retVal ):
        if retVal: return self.vdomdynobj.top
        else: self.vdomdynobj.top = str(value)

    @AutoCast
    @v_PropertySimple
    def v_left( self, value, retVal ):
        if retVal: return self.vdomdynobj.left
        else: self.vdomdynobj.left = str(value)

    @AutoCast
    @v_PropertySimple
    def v_height( self, value, retVal ):
        if retVal: return self.vdomdynobj.height
        else: self.vdomdynobj.height = str(value)

    @AutoCast
    @v_PropertySimple
    def v_width( self, value, retVal ):
        if retVal: return self.vdomdynobj.width
        else: self.vdomdynobj.width = str(value)


class v_growl( generic ):

    def __init__( self ):
        self.message = ""
        self.title   = ""


    @AutoCast
    def __call__( self, title, message ):
        self.message = message
        self.title = title



class v_dbdictionary( generic ):

    __DB_NAME = "kv_macro_storage"


    def __init__( self, namespace ):
        generic.__init__( self )
        self.__namespace = namespace


    def __call__( self, *arguments, **keywords ):
        if "let" in keywords:
            return self.let(*arguments, **keywords)
        elif "set" in keywords:
            raise errors.type_mismatch
        else:
            return self.get(*arguments, **keywords)


    @AutoCast
    def get( self, key ):
        row = Database.macrosdb().fetch_one(
                "SELECT value FROM `{0}` WHERE key=? AND namespace=?".format( v_dbdictionary.__DB_NAME ),
                (  key , self.__namespace ) )
        return row[0] if row else None


    @AutoCast
    def let( self, key = None, *arguments, **keywords ):
        if not key: raise errors.wrong_number_of_arguments
        Database.macrosdb().commit(
                "REPLACE INTO `{0}` (key, value, namespace) VALUES (?, ?, ?)".format( v_dbdictionary.__DB_NAME ),
                (  key , keywords[ "let" ], self.__namespace ) )


    @AutoCast
    def v_remove( self, key ):
        self.erase( key )


    @AutoCast
    def erase( self, key ):
        Database.macrosdb().commit(
                "DELETE FROM `{0}` WHERE key=? AND namespace=?".format( v_dbdictionary.__DB_NAME ),
                (  key, self.__namespace ) )


    @AutoCast
    def __contains__( self, key ):
        return bool( Database.macrosdb().fetch_one(
                "SELECT value FROM `{0}` WHERE key=? AND namespace=?".format( v_dbdictionary.__DB_NAME ),
                (  key , self.__namespace ) ) )


    @AutoCast
    def v_keys( self ):
        return  [ row[0] for row in Database.macrosdb().fetch_all(
                "SELECT key FROM `{0}` WHERE namespace=?".format( v_dbdictionary.__DB_NAME ),
                (  self.__namespace, ) ) ]


    @AutoCast
    def v_items( self ):
        return  [ (row[0], row[1] ) for row in Database.macrosdb().fetch_all(
                "SELECT key, value FROM `{0}` WHERE namespace=?".format( v_dbdictionary.__DB_NAME ),
                (  self.__namespace, ) ) ]


    def __iter__( self ):
        for key in self.v_keys():
                yield key




class v_session_dictionary( generic ):

    def __init__( self, namespace ):
        generic.__init__( self )
        self.session_db = session[ namespace ] = session.get( namespace, {} )


    def __call__( self, *arguments, **keywords ):
        if "let" in keywords:
            return self.let( *arguments, **keywords )
        elif "set" in keywords:
            return self.set( *arguments, **keywords )
        else:
            return self.get( *arguments, **keywords )


    @AutoCast
    def get( self, key, secure = True, *arguments, **keywords ):
        db = self.session_db if secure else session
        return db.get( key, None )


    def let( self, key = None, secure = True, *arguments, **keywords ):
        db = self.session_db if secure else session
        db[ key.as_string ] = keywords[ "let" ]


    def set( self, key = None, secure = True, *arguments, **keywords ):
        db = self.session_db if secure else session
        db[ key.as_string ] = keywords[ "set" ]


    @AutoCast
    def v_remove( self, *args, **kwargs  ):
        self.erase( *args, **kwargs )


    @AutoCast
    def erase( self, key, secure = True ):
        db = self.session_db if secure else session
        if key in db: del db[ key ]


    @AutoCast
    def __contains__( self, key ):
        return key in self.session_db


    @AutoCast
    def v_keys( self, secure = True ):
        db = self.session_db if secure else session
        return db.keys()


    @AutoCast
    def v_items( self, secure = True ):
        return self.session_db.items()


    def __iter__( self ):
        for key in self.v_keys():
                yield key



class v_buffer( generic ):

    def __init__( self, inst = None ):
        self._handler = inst


    @CachedProperty
    def handler( self ):
        return self._handler if  self._handler else self.open()


    def open( self ):
        return cStringIO.StringIO()

    @classmethod
    def v_create( self ):
        #old implementation. Use 'set b = new buffer'
        return self()


    @AutoCast
    def v_write( self, line ):
        self.handler.write( encodeUTF8( line ) )

    @AutoCast
    def v_writelines( self, lines ):
        self.handler.writelines( map( encodeUTF8, lines ) )


    @AutoCast
    def v_read( self, size = -1 ):
        return decodeUTF8( self.handler.read( size ) )


    @AutoCast
    def v_readline( self, size = -1 ):
        return decodeUTF8( self.handler.readline( size ) )


    @AutoCast
    def v_readlines( self, size = -1 ):
        return map( decodeUTF8, self.handler.readlines( size ) )


    @AutoCast
    def v_seek( self, offset, whence = 0 ):
        self.handler.seek( offset, whence )


    @AutoCast
    def v_tell( self ):
        return self.handler.tell()


    @AutoCast
    def v_truncate( self, size = None ):
        self.handler.truncate( size )


    def get_value( self ):
        self.handler.seek( 0 )
        data = decodeUTF8( self.handler.read() )
        self.handler.seek( 0 )
        return data


    @AutoCast
    def v_getvalue( self ):
        return self.get_value()


    def v_getbinary( self ):
        return binary( self.get_value() )


    @AutoCast
    def v_frombinary( self, data ):
        self.handler.write( data )


    def v_close( self ):
        self.handler.close()


    @AutoCast
    def v_insertbom( self, codec_name = "utf8" ):
        import codecs
        codec = codecs.BOM_UTF8
        current = self.handler.tell()
        self.handler.seek(0)
        self.handler.write(codec)
        self.handler.seek( current + len( codec ) )



date_format = "%d.%m.%Y %H:%M:%S"
def date_from_vdate( value ):
    from vscript.subtypes.date import decode_date
    return datetime( *decode_date( value ) )



def date_to_vdate( value ):
    from vscript.subtypes.date import encode_date, date
    return date( encode_date( *list( value.timetuple() )[:6] ) )



@AutoCast
def v_formatdate( template, date ):
    return date.strftime( template )



@AutoCast
def v_datefromstring( date_string, template = None):
    if not template: template = date_format
    return datetime.strptime( date_string, template )



@AutoCast
def v_base64encode( line ):
    return base64.b64encode( line.encode("utf8") )



@AutoCast
def v_base64decode( line ):
    return base64.b64decode( line ).decode("utf8")



@AutoCast
def v_md5( line ):
    return md5( line ).hexdigest()



@AutoCast
def v_formatstring( template, *args ):
    if len( args ) == 0: return template
    elif len( args ) == 1 and is_dict( args[ 0 ] ):
        return template.format( **args[ 0 ] )
    else: return template.format( *args )



class v_event( base_object ):

    @CachedProperty
    def event( self ):
        return self.object



class v_customevent( v_event ):

    def __init__( self ):
        from VEE_events import VEE_CustomEvent
        v_event.__init__( self, VEE_CustomEvent() )


    @AutoCast
    @v_PropertySimple
    def v_name( self, value, retVal ):
        if retVal:
            return self.event.name
        else:
            self.event.name = value


    @AutoCast
    @v_PropertySimple
    def v_data( self, value, retVal ):
        if retVal:
            return self.event.data
        else:
            self.event.data = value



@AutoCast
def v_raiseevent( event_obj, disp ):

    if not isinstance( event_obj, v_customevent ):
        raise v_BadObjectType( "Event must be CustomEvent or APIEvent type, not %s" % event_obj.__class__.__name__ )

    if event_obj.event.name:
        event_obj.event.plugin_guid = disp.namespace
        event_obj.event.activate()
    else:
        raise v_BadObjectType( "Set event name" )



class v_timer( base_object ):

    @CachedProperty
    def timer( self ):
        return self.object


    @AutoCast
    @v_PropertySimple
    def v_delay( self, value, retVal ):
        if retVal:
            return ":".join( map( str, self.timer.delay ) )
        else:
            self.timer.delay = map( int, value.split( ":" ) )


    @AutoCast
    @v_PropertySimple
    def v_isactive( self, value, retVal ):
        if retVal:
            return self.timer.active
        else:
            self.timer.active = value


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_lastrun( self ):
        return self.timer.last_run


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_name( self ):
        #timer name is GUID:name
        return self.timer.name.split( ":", 1 )[ 1 ]


    #obsolete methods names
    v_is_active = v_isactive
    v_last_run  = v_lastrun



class v_TimerDoesntExists( v_BaseException ):
    pass



class v_engine( object ):

    @staticmethod
    @AutoCast
    def v_activatetimer( timer_name, disp ):
        try:
            disp.activate_timer( timer_name )
        except:
            raise v_TimerDoesntExists( "Timer doesn't exists" )


    @staticmethod
    @AutoCast
    def v_deactivatetimer( timer_name, disp ):
        try:
            disp.deactivate_timer( timer_name )
        except:
            raise v_TimerDoesntExists( "Timer doesn't exists" )


    @staticmethod
    @AutoCast
    def v_gettimer( timer_name, disp ):
        t = disp.get_timer_by_name( timer_name )
        if not t: raise v_TimerDoesntExists( "Timer doesn't exists" )
        return v_timer( t )



class v_currentpage( generic ):

    def __init__( self ):
        generic.__init__( self )
        self.page_name = ""
        self.redirect_url = ""
        self.namespace = ""


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_host( self ):
        return "{0}://{1}".format(
                    "https" if request.environment.get( 'SERVER_PORT', '80' ) == '443' else request.protocol.name.lower(),
                    request.server.host )


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_lang( self ):
        return session.get( "lang" )


    @AutoCastCachedProperty
    @v_PropertyReadOnly
    def v_name( self ):
        return self.page_name


    @AutoCast
    def v_redirect( self, url ):
        self.redirect_url = url


    def v_refresh( self ):
        self.v_redirect( "/" + self.page_name )


    def __call__( self, *arguments, **keywords ):
        if "let" in keywords:
            return self.let(*arguments, **keywords)
        elif "set" in keywords:
            raise errors.type_mismatch
        else:
            return self.get(*arguments, **keywords)


    def _format_key( self, key ):
        return u"{0}_{1}".format( self.namespace, key )

    @AutoCast
    def get( self, key, secure = True, *arguments, **keywords ):
        if not key: raise errors.wrong_number_of_arguments
        return request.shared_variables[ self._format_key( key ) if secure else key ]


    @AutoCast
    def let( self, key = None, secure = True, *arguments, **keywords ):
        if not key: raise errors.wrong_number_of_arguments
        response.shared_variables[ self._format_key( key ) if secure else key ] = keywords[ "let" ]


    @AutoCast
    def erase( self, key, secure = True ):
        if not key: raise errors.wrong_number_of_arguments
        response.shared_variables[ self._format_key( key ) if secure else key ] = None


    @AutoCast
    def __contains__( self, key ):
        if not key: raise errors.wrong_number_of_arguments
        return self._format_key( key ) in request.shared_variables.keys()




class v_plugin( base_object ):

    def __init__( self, guid ):
        base_object.__init__( self, self )
        #self.name = ""
        self.guid = guid


class v_macros( base_object ):

    def __init__( self, guid, name ):
        base_object.__init__( self, self )
        self.macro_name = name
        self.guid = guid

    @AutoCast
    def v_name( self ):
        return self.macro_name

    @AutoCast
    def v_guid( self ):
        return self.guid


def v_exitscript():
    from VEE_tools import StopExecutionError
    raise StopExecutionError()


@AutoCast
def v_escapestring( data, quote = False ):
    return escape( data, quote )


environment = (
    (   "v_generateguid"            , v_generateguid    ),
    (   "v_generate_guid"           , v_generateguid    ),
    (   "v_buffer"                  , v_buffer          ),
    (   "v_base64encode"            , v_base64encode    ),
    (   "v_base64decode"            , v_base64decode    ),
    (   "v_md5"                     , v_md5             ),
    (   "v_formatstring"            , v_formatstring    ),
    (   "v_datefromstring"          , v_datefromstring  ),
    (   "v_formatdate"              , v_formatdate      ),
    (   "v_exitscript"              , v_exitscript      ),
    (   "v_escapestring"            , v_escapestring    ),
    #Exceptions
    (   "v_baseexception"               , error( v_BaseException                )   ),
    (   "v_badobjecttype"               , error( v_BadObjectType                )   ),
    (   "v_timerdoesntexists"           , error( v_TimerDoesntExists            )   ),
)

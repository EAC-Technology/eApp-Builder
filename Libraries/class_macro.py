from class_db import Database
from utils.uuid import uuid4
from collections import OrderedDict
import base64
import re

_SQL_TABLE_NAME = "macros"
_SQL_SELECT_HEADER = """
            SELECT
                id,
                code,
                name,
                class_name,
                is_button_macros,
                on_board,
                picture,
                guid,
                page,
                description,
                zindex,
                timer_guid,
                plugin_guid,
                namespace,
                page,
                custom_event_guid,
                type
            FROM `{0}` """.format( _SQL_TABLE_NAME )


LIB_NAME_REGEXP = re.compile(r"^'#include\((\w+)\)", flags=re.MULTILINE)


class Macros ( object ):

    class MacrosType(object):
        BUTTON = "button"
        EVENT  = "event"
        LIBRARY= "library"
        UNKNOWN= "unknown"

    def __init__( self ):
        self.id                 = None
        self.name               = None
        self.code               = ""
        self.class_name         = None
        self.is_button_macros   = None
        self.on_board           = None
        self.macros_picture     = None
        self.guid               = None
        self.page               = None
        self.description        = None
        self.zindex             = None
        self.timer_guid         = None
        self.namespace          = None
        self.plugin_guid        = None
        self.page               = None
        self.custom_event_guid  = None
        self.type               = self.MacrosType.UNKNOWN


    def get_plugin_guid( self ):
        return self.__plugin_guid

    def set_plugin_guid( self, value ):
        self.__plugin_guid = self.namespace = value

    plugin_guid = property( get_plugin_guid, set_plugin_guid )

    def __fill_from_row( self, row ):
        self.id                 = row[0]
        self.code               = row[1] or ""
        self.name               = row[2]
        self.class_name         = row[3]
        self.is_button_macros   = row[4]
        self.on_board           = row[5]
        self.macros_picture     = row[6]
        self.guid               = row[7]
        self.page               = row[8]
        self.description        = row[9]
        self.zindex             = row[10]
        self.timer_guid         = row[11]
        self.plugin_guid        = row[12]
        self.namespace          = row[13]
        self.page               = row[14]
        self.custom_event_guid  = row[15]
        self.type               = row[16]

        if not self.type or self.type == self.MacrosType.UNKNOWN:
            self.type = self.MacrosType.BUTTON if self.is_button_macros == "1" else \
                        self.MacrosType.EVENT


        return self


    def register_macro( self ):
        register_macro( self )


    def unregister_macro( self ):
        unregister_macro( self )


    def save( self ):
        (self.__update if self.id else self.__insert)()
        #raise Exception(self.type)
        self.register_macro()
        return self


    def __insert(self):
        self.guid = str( uuid4() ) if self.guid is None else self.guid
        self.id = Database.macrosdb().commit(
            "INSERT INTO macros (name, code, class_name, is_button_macros,"
            "on_board, picture, guid, page, description, zindex, timer_guid,"
            "plugin_guid, namespace, page, custom_event_guid,type) VALUES"
            "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
             ( self.name, self.code, self.class_name, self.is_button_macros,
             self.on_board, self.macros_picture, self.guid, self.page,
             self.description, self.zindex, self.timer_guid,
             self.plugin_guid, self.plugin_guid, self.page,
             self.custom_event_guid, self.type ) )

        return self


    def delete( self ):
        Database.macrosdb().commit("""DELETE FROM macros WHERE id=?""", (self.id,))
        self.unregister_macro( )
        self.id = None


    def __update(self):
        Database.macrosdb().commit(
            """UPDATE macros
                SET
                    name=?,
                    code=?,
                    class_name=?,
                    is_button_macros=?,
                    on_board=?,
                    picture=?,
                    guid=?,
                    page=?,
                    description=?,
                    zindex=?,
                    timer_guid=?,
                    plugin_guid=?,
                    namespace=?,
                    page=?,
                    custom_event_guid=?,
                    type=?
                    WHERE id=?""",
             (self.name, self.code, self.class_name, self.is_button_macros,
             self.on_board, self.macros_picture, self.guid, self.page,
             self.description, self.zindex, self.timer_guid, self.plugin_guid,
             self.namespace, self.page, self.custom_event_guid,
             self.type, self.id))

        return self


    @classmethod
    def get_all(self):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER, )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []

    @classmethod
    def get_all_event_macros(self):
        db_rows = Database.macrosdb().fetch_all(    _SQL_SELECT_HEADER +
            "WHERE class_name<>''", )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []


    @classmethod
    def get_all_on_board(self):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE on_board='1'", )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []

    @classmethod
    def get_all_button(self):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE is_button_macros='1' AND on_board='0'", )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []

    @classmethod
    def get_all_non_event(self):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE is_button_macros='1'", )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []


    @classmethod
    def get_all_non_library(self):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE type<>?", (self.MacrosType.LIBRARY,) )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []



    @classmethod
    def get_by_id(self, id):
        db_row = Database.macrosdb().fetch_one( _SQL_SELECT_HEADER +
            "WHERE id=?", (id, ))

        return self().__fill_from_row(db_row) if db_row else None

    @classmethod
    def get_by_guid(self, guid):
        db_row = Database.macrosdb().fetch_one( _SQL_SELECT_HEADER +
            "WHERE guid=?", (guid, ))

        return self().__fill_from_row(db_row) if db_row else None

    @classmethod
    def get_macros_by_plugin_guid(self, plugin_guid):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE plugin_guid=?", ( plugin_guid, ) )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []


    @classmethod
    def get_macros_by_timer_guid(self, timer_guid):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE timer_guid=?", ( timer_guid, ) )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []

    @classmethod
    def get_macros_by_custom_event_guid(self, custom_event_guid):
        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE custom_event_guid=?", ( custom_event_guid, ) )

        return [self().__fill_from_row(row) for row in db_rows] if db_rows else []



    @classmethod
    def get_config_macro(self, plugin_guid):
        db_row = Database.macrosdb().fetch_one( _SQL_SELECT_HEADER +
            "WHERE plugin_guid=? AND name='config'", ( plugin_guid, ) )

        return self().__fill_from_row(db_row) if db_row else None

    @classmethod
    def export(self, id_list):
        from StringIO import StringIO

        outp = StringIO()
        outp.write("<macros>\n")
        for id in id_list:
             macros = self.get_by_id(id)

             outp.write(macros.generate_xml())

        outp.write("</macros>")
        return outp


    def get_xmlnode(self):
        from class_xml_macro import XMLMacros
        import base64
        xml = XMLMacros()
        xml.name            = self.name
        xml.source          = self.code
        xml.class_name      = self.class_name
        xml.is_button       = self.is_button_macros if self.is_button_macros else "0"
        xml.on_board        = self.on_board if self.on_board else "0"
        xml.macros_picture  = base64.b64encode(application.storage.readall(self.macros_picture)) if self.macros_picture else ""
        xml.description     = self.description
        xml.guid            = self.guid
        xml.timer_guid      = self.timer_guid
        xml.custom_event_guid = self.custom_event_guid
        xml.page            = self.page

        if not self.type or self.type == self.MacrosType.UNKNOWN:
            self.type = self.MacrosType.BUTTON if self.is_button_macros == "1" else \
                        self.MacrosType.EVENT

        xml.type            = self.type

        return xml
        #xml.save()

    def generate_xml(self):
        return self.get_xmlnode().toprettyxml().encode("utf8")


    def fill_from_xml(self, xml, plugin_guid):
        self.name           = xml.name
        self.code           = xml.source
        self.class_name     = xml.class_name
        self.is_button_macros = xml.is_button
        self.on_board       = xml.on_board
        self.guid               = xml.guid
        self.timer_guid         = xml.timer_guid
        self.custom_event_guid  = xml.custom_event_guid
        self.description        = xml.description
        self.plugin_guid        = plugin_guid
        self.page               = xml.page
        self.type               = xml.type

        if not self.type or self.type == self.MacrosType.UNKNOWN:
            self.type = self.MacrosType.BUTTON if self.is_button_macros == "1" else \
                        self.MacrosType.EVENT


        picture_name = ""
        self.macros_picture = ""
        if xml.macros_picture:
            self.macros_picture = picture_name = str(uuid4())
            application.storage.write(picture_name, base64.b64decode(xml.macros_picture))

        self.save()


    def libraries(self):
        lib_names = LIB_NAME_REGEXP.findall(self.code)
        if not lib_names: return []

        lib_names = OrderedDict.fromkeys([n.lower() for n in lib_names])

        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            "WHERE plugin_guid=? and type=?", (self.plugin_guid, self.MacrosType.LIBRARY) )

        libraries = [Macros().__fill_from_row(row) for row in db_rows] if db_rows else []

        for lib in libraries:
            if lib.name.lower() in lib_names:
                lib_names[lib.name.lower()] = lib

        return [lib for lib in lib_names.values() if lib is not None]



    @classmethod
    def update_all_macro_with_library(cls, library):

        db_rows = Database.macrosdb().fetch_all( _SQL_SELECT_HEADER +
            """WHERE plugin_guid=? and code LIKE "%'#include("||?||")%" """, (library.plugin_guid, library.name) )

        return map( register_macro, [cls().__fill_from_row(row) for row in db_rows] if db_rows else [] )



def register_all_event_macro( ):
    map( register_macro, Macros.get_all_non_library() )



def register_macro( macro ):
    import VEE_events

    if macro.type == macro.MacrosType.LIBRARY:
        Macros.update_all_macro_with_library(macro)
        return

    event_class =   VEE_events.VEE_ButtonEvent if macro.type == macro.MacrosType.BUTTON else \
                    getattr( VEE_events, macro.class_name, None )

    if not event_class: return

    if event_class == VEE_events.VEE_TimerEvent:
        from class_timer import Timer
        Timer.register_timer_by_guid( macro.timer_guid )
        data = (macro.timer_guid,)

    elif event_class == VEE_events.VEE_CustomEvent:
        from class_custom_event import CustomEvent
        custom_event = CustomEvent.get_custom_event_by_guid(macro.custom_event_guid)
        data = (custom_event.plugin_guid, custom_event.name)

    elif event_class == VEE_events.VEE_ButtonEvent:
        data = (macro.namespace, macro.guid)

    else:
        data = (None,)

    key = event_class.get_key(*data)

    from VEE_vmacro_dispatcher import VEE_vmacro_dispatcher
    from VEE_core import engine
    dispatcher = VEE_vmacro_dispatcher(macro)
    engine.register_dispatcher(event_class, key, dispatcher)



def unregister_macro(macro):
    import VEE_events

    if macro.type == macro.MacrosType.LIBRARY:
        Macros.update_all_macro_with_library(macro)
        return

    event_class =   VEE_events.VEE_ButtonEvent if macro.type == macro.MacrosType.BUTTON else \
                    getattr( VEE_events, macro.class_name, None )

    if not event_class: return

    if event_class == VEE_events.VEE_TimerEvent:
        from class_timer import Timer
        Timer.register_timer_by_guid( macro.timer_guid )
        data = (macro.timer_guid,)

    elif event_class == VEE_events.VEE_CustomEvent:
        from class_custom_event import CustomEvent
        custom_event = CustomEvent.get_custom_event_by_guid( macro.custom_event_guid )
        data = (custom_event.plugin_guid, custom_event.name)

    elif event_class == VEE_events.VEE_ButtonEvent:
        data = (macro.namespace, macro.guid)

    else:
        data = (None,)

    key = event_class.get_key(*data)

    from VEE_core import engine
    engine.unregister_dispatcher(event_class, key, macro.guid)

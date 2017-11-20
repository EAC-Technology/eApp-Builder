"""
"""

DEFAULT_LANG_REQ_NAME = "_ln_"
DEFAULT_LANGUAGE = "en_US"


def get_lang():
    """
    """
    lang = DEFAULT_LANGUAGE

    if DEFAULT_LANG_REQ_NAME in request.arguments:
        lang = request.arguments[DEFAULT_LANG_REQ_NAME]

    elif "lang" in session:
        lang = session["lang"]

    elif "HTTP_ACCEPT-LANGUAGE" in request.environment:
        lang = request.environment["HTTP_ACCEPT-LANGUAGE"]

    session["lang"] = lang[:2]
    return session["lang"]


###############################################################################

DEFAULT_LOC_PROPERTIES = [ "title", "label", "text", "value" ]


class LocalizationError(Exception):
    pass


class LocalizationAttrNotFound(LocalizationError):
    def __init__(self, obj_name, prop):
        LocalizationError.__init__(
            self,
            u"Can't find property '{prop}' for object '{obj_name}'".format(
                prop=prop,
                obj_name=obj_name
            )
        )


class LocalizationDefaultAttrNotFound(LocalizationAttrNotFound):
    def __init__(self, obj_name):
        LocalizationAttrNotFound.__init__(
            self,
            obj_name=obj_name,
            prop=u" or ".join(DEFAULT_LOC_PROPERTIES)
        )


def localize_string(localization_source, loc_args):
    """
    """
    loc_key, format_args = (loc_args, None) if isinstance(loc_args, basestring) else loc_args
    loc_text = localization_source[loc_key]
    if format_args:
        loc_text = loc_text.format(**format_args)

    return loc_text


def localize_object(obj, loc_text, prop=None):
    """
    """
    if not prop:
        for default_prop in DEFAULT_LOC_PROPERTIES:
            if hasattr(obj, default_prop):
                prop = default_prop
                break

        else:
            raise LocalizationDefaultAttrNotFound(obj.name)

    elif not hasattr(obj, prop):
        raise LocalizationAttrNotFound(obj.name, prop)

    setattr(obj, prop, loc_text)


def localize(loc_objects, localization_source):
    """Localize objects.
        - @objects is dict like:
        {
            vdom_object | [vdom_object, vdom_object] : localization_key,
            vdom_object | [vdom_object, vdom_object] : {
                property: localization_key
            },
            vdom_object | [vdom_object, vdom_object] : {
                property: [
                    localization_key,
                    dict of named arguments for ".format"
                ]

            },
            vdom_object | [vdom_object, vdom_object] : [
                localization_key,
                dict of named arguments for ".format"
            ]
        }
    """

    # 2 cycles for optimization
    for objects, loc_data in loc_objects.iteritems():
        objects = objects if isinstance(objects, (list, tuple)) else (objects,)

        if isinstance(loc_data, dict):
            for prop, loc_data in loc_data.items():
                text = localize_string(localization_source, loc_data)
                for obj in objects:
                    localize_object(obj, text, prop)


        else:
            text = localize_string(localization_source, loc_data)
            for obj in objects:
                localize_object(obj, text)


class Localization(object):

    def __init__(self, loc_source=None, controls=None):
        self.controls = controls or {}
        self.localization = loc_source

    def localize(self):
        localize(self.controls, self)

    def __getitem__(self, key):
        return self.localization.get(key, key)

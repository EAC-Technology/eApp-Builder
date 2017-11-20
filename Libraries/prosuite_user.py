"""
"""

import ProAdmin


class ProSuiteUser(object):

    def __init__(self, proadmin_user):
        self._user = proadmin_user

    def __hash__(self):
        return hash(self.guid)

    def __eq__(self, other):
        return self.guid == other.guid

    @property
    def user(self):
        return self._user

    @property
    def guid(self):
        return self.user.guid

    @property
    def name(self):
        return self.user.name

    @property
    def notification_email(self):
        return self.user.notification_email

    def is_admin(self):
        return bool(ProAdmin.application().rules(subject=self.user, access="a"))

    @classmethod
    def current_user(cls):
        """
        Return logged in user
        """
        proadmin_user = ProAdmin.current_user()
        return cls(proadmin_user) if proadmin_user else None

    @classmethod
    def get_by_guid(cls, guid):
        """
        Find user by GUID
        """
        proadmin_user = ProAdmin.application().get_users(guid=guid)
        return cls(proadmin_user[0]) if proadmin_user else None

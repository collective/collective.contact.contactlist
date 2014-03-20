from zope.interface import Interface
from five import grok
from collective.contact.contactlist.interfaces import IUserLists
from plone import api as ploneapi
from collective.contact.contactlist.content.contactlist import IContactList
from zope.security.management import checkPermission


class  UserListStorage(grok.MultiAdapter):
    grok.adapts(Interface, Interface, Interface)
    grok.implements(IUserLists)

    def __init__(self, user, portal, request):
        self.user = user
        self.portal = portal
        self.request = request

    def get_lists_brains(self):
        """Get brains of lists user can use
        """
        ctool = ploneapi.portal.get_tool('portal_catalog')
        brains = ctool.searchResults(object_provides=IContactList.__identifier__)
        return brains

    def get_lists(self):
        """Get lists user can use
        """
        return [b.getObject() for b in self.get_lists_brains()]

    def get_editable_lists(self):
        return [o for o in self.get_lists()
                if checkPermission('cmf.ModifyPortalContent', o)]

    def get_container(self):
        """Get lists container
        """
        user_id = self.user.getId()
        if not user_id:
            return None

        return self.portal.Members.get(user_id, None)
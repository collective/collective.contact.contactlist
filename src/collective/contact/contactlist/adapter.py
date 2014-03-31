from zope.interface import Interface, implements
from zope.component import adapts
from plone import api as ploneapi
from collective.contact.contactlist.interfaces import IUserLists
from collective.contact.contactlist.content.contactlist import IContactList


class  UserListStorage(object):
    adapts(Interface, Interface, Interface)
    implements(IUserLists)

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
        """Lists user can edit
        """
        mtool = ploneapi.portal.get_tool('portal_membership')
        return [o for o in self.get_lists()
                if mtool.checkPermission('Modify portal content', o)]

    def get_my_lists(self):
        """Lists created by user
        """
        container = self.get_container()
        return [o for o in container.values() if IContactList.providedBy(o)]

    def get_container(self):
        """Get lists container
        """
        user_id = self.user.getId()
        if not user_id:
            return None

        return self.portal.Members.get(user_id, None)
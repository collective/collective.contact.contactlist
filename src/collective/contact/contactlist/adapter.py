from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.component import adapts
from zope.interface import Interface, implements
from zope.intid.interfaces import IIntIds

from plone import api as ploneapi

from collective.contact.contactlist.interfaces import IUserLists, IContactList


class UserListStorage(object):
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

    def get_lists_for_contact(self, contact):
        """Get lists that contain contact.
        """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        contact_intid = intids.queryId(contact)
        query = {'to_id': contact_intid,
                 'from_interfaces_flattened': IContactList,
                 'from_attribute': 'contacts'}
        return [rel.from_object for rel in catalog.findRelations(query)]

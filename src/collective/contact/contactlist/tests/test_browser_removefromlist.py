from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.api import get_contacts
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login


class TestRemoveFromList(IntegrationTestCase):

    def test_call(self):
        portal = self.portal
        army = portal.mydirectory.armeedeterre
        login(portal, "testuser")
        contact_list = create_list("My list", "", [army.corpsa, army.corpsb])
        removeview = contact_list.restrictedTraverse("@@contactlist.remove-from-list")
        removeview.request["REQUEST_METHOD"] = "POST"
        removeview.request["uids"] = [army.corpsb.UID()]
        removeview()
        self.assertEqual(get_contacts(contact_list), [army.corpsa])

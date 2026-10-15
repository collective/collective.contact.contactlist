from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.browser.excelexport import ContactListDataSource
from collective.contact.contactlist.browser.excelexport import ExportLinkViewlet
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.testing import PLONE_MAJOR
from plone import api
from plone.app.testing import login


class TestExportLinkViewlet(IntegrationTestCase):

    def test_render(self):
        login(self.portal, "testuser")
        contact_list = create_list(
            "Exported", "", [self.portal.mydirectory.armeedeterre]
        )
        viewlet = ExportLinkViewlet(contact_list, self.layer["request"], None)
        viewlet.update()
        html = viewlet.render()
        self.assertIn(
            'href="http://nohost/plone/Members/testuser/exported/@@collective.excelexport"',
            html,
        )
        if PLONE_MAJOR < 5:
            # skin image of Products.MimetypesRegistry
            self.assertIn('src="http://nohost/plone/xls.png"', html)
        else:
            # the xls.png image of Plone 4 doesn't exist anymore
            self.assertIn('src="http://nohost/plone/++plone++', html)


class TestContactListDataSource(IntegrationTestCase):

    def test_get_filename(self):
        login(self.portal, "testuser")
        contact_list = create_list("Exported", "", [])
        self.assertEqual(
            ContactListDataSource(contact_list, self.layer["request"]).get_filename(),
            "exported.xls",
        )

    def test_get_objects(self):
        login(self.portal, "testuser")
        army = self.portal.mydirectory.armeedeterre
        contact_list = create_list("Exported", "", [army.corpsa, army.corpsb])
        source = ContactListDataSource(contact_list, self.layer["request"])
        self.assertEqual(source.get_objects(), [army.corpsa, army.corpsb])
        # a deleted contact is skipped
        api.content.delete(army.corpsb, check_linkintegrity=False)
        self.assertEqual(source.get_objects(), [army.corpsa])

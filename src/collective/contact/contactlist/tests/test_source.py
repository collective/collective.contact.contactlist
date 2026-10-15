from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.source import ContactListSourceBinder
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login


class TestContactListSource(IntegrationTestCase):

    def assertTermsMatchContents(self, terms, contents):
        self.assertEqual(
            sorted([t.token for t in terms]),
            sorted(["/".join(c.getPhysicalPath()) for c in contents]),
        )

    def test_search(self):
        portal = self.portal
        login(portal, "testuser")
        army = portal.mydirectory.armeedeterre
        create_list(
            "Corpses",
            "Description of my list",
            [army.corpsa, army.corpsb],
            subject=["test-subject"],
        )
        create_list(
            "Corpses 2",
            "Description of my list",
            [army.corpsb],
            subject=["test-subject"],
        )
        create_list(
            "Divisions",
            "Description of my list",
            [army.corpsa.divisionalpha, army.corpsa.divisionbeta],
            subject=["test-subject-2"],
        )

        # or operator works
        source = ContactListSourceBinder(
            contact_lists_query={"Subject": "test-subject"},
            contact_lists_operator="or",
            portal_type="organization",
        )(portal)
        self.assertTermsMatchContents(source.search(""), [army.corpsa, army.corpsb])

        # and operator works
        source = ContactListSourceBinder(
            contact_lists_query={"Subject": "test-subject"},
            contact_lists_operator="and",
            portal_type="organization",
        )(portal)
        self.assertTermsMatchContents(source.search(""), [army.corpsb])

        # combines well with content filter
        source = ContactListSourceBinder(
            contact_lists_query={"id": "corpses"}, getId="corpsb"
        )(portal)
        self.assertTermsMatchContents(source.search(""), [army.corpsb])

        # combines well with specific query filter
        source = ContactListSourceBinder(
            contact_lists_query={"Subject": "test-subject"},
            contact_lists_operator="or",
            portal_type="organization",
        )(portal)
        self.assertTermsMatchContents(
            source.search("path:/mydirectory/armeedeterre/corpsb"), [army.corpsb]
        )

        # works without content filter
        source = ContactListSourceBinder(contact_lists_query={"id": "corpses-2"})(
            portal
        )
        self.assertTermsMatchContents(source.search(""), [army.corpsb])

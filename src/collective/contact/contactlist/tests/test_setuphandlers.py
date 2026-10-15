from collective.contact.contactlist.setuphandlers import post_install
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.testing import PLONE_MAJOR
from plone import api

import unittest


class TestSetuphandlers(IntegrationTestCase):

    @unittest.skipIf(
        PLONE_MAJOR < 5,
        "Plone 4 creates the Members folder with the site: post_install only sets "
        "memberareaCreationFlag from the profile context (checked in test_setup)",
    )
    def test_post_install(self):
        # the Members folder is created on install
        self.assertIn("Members", self.portal)
        # it is recreated when missing, as on a site created without the example content
        api.content.delete(self.portal.Members, check_linkintegrity=False)
        post_install(None)
        self.assertEqual(self.portal.Members.getLayout(), "@@member-search")
        # an existing Members folder is kept
        self.portal.Members.setTitle("My members")
        post_install(None)
        self.assertEqual(self.portal.Members.Title(), "My members")

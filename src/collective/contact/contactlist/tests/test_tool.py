# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone import api
from plone.app.testing import login
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID

from collective.contact.contactlist.api import create_list, update_list,\
    get_contacts
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.api import get_user_lists_adapter
from collective.contact.contactlist.vocabularies import MyListsVocabulary,\
    ListsVocabulary


class TestInstall(IntegrationTestCase):
    """Test installation of collective.contact.contactlist into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.contact.contactlist is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.contact.contactlist'))

    def test_uninstall(self):
        """Test if collective.contact.contactlist is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.contact.contactlist'])
        self.assertFalse(self.installer.isProductInstalled('collective.contact.contactlist'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveContactContactlistLayer is registered."""
        from collective.contact.contactlist.interfaces import ICollectiveContactContactlistLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveContactContactlistLayer, utils.registered_layers())

    def test_create_list(self):
        portal = self.portal
        login(portal, TEST_USER_NAME)
        directory = portal.mydirectory
        contacts = [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb]
        create_list("Corpses", "Description of my list", contacts)
        user_folder = portal.Members[TEST_USER_ID]
        self.assertIn('corpses', user_folder)
        self.assertEqual(len(user_folder.corpses.contacts), 2)
        update_list(user_folder.corpses, [directory.armeedeterre.corpsa,
                                          directory.armeedeterre.corpsa.divisionalpha])
        self.assertEqual(len(user_folder.corpses.contacts), 3)
        contacts = get_contacts(user_folder.corpses)
        self.assertEqual(len(contacts), 3)
        self.assertIn(directory.armeedeterre.corpsa, contacts)

    def test_adapter(self):
        portal = self.portal
        directory = portal.mydirectory
        login(portal, TEST_USER_NAME)
        contacts = [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb]
        list_1 = create_list("Corpses", "Description of my list", contacts)

        login(portal, 'testuser')
        contacts = [directory.armeedeterre.corpsa.divisionalpha,
                    directory.armeedeterre.corpsb]
        list_2 = create_list("Divisions", "Description of my list", contacts)

        adapter = get_user_lists_adapter()
        self.assertEqual(adapter.get_lists(), [list_1, list_2])

        self.assertEqual(adapter.get_my_lists(), [list_2])

        self.assertEqual(adapter.get_editable_lists(), [list_1, list_2])

    def test_vocabularies(self):

        portal = self.portal
        directory = portal.mydirectory
        login(portal, TEST_USER_NAME)
        contacts = [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb]
        list_1 = create_list("Corpses", "Description of my list", contacts)

        login(portal, 'testuser')
        contacts = [directory.armeedeterre.corpsa.divisionalpha,
                    directory.armeedeterre.corpsb]
        list_2 = create_list("Divisions", "Description of my list", contacts)

        my_lists_vocabulary = getUtility(IVocabularyFactory,
                                         name=MyListsVocabulary.name())(portal)
        self.assertEqual(len(my_lists_vocabulary._terms), 1)

        lists_vocabulary = getUtility(IVocabularyFactory,
                                         name=ListsVocabulary.name())(portal)
        self.assertEqual(len(lists_vocabulary._terms), 2)
        self.assertEqual(lists_vocabulary._terms[0].title, "Divisions")
        self.assertEqual(lists_vocabulary._terms[1].title, "Corpses (%s)" % TEST_USER_ID)
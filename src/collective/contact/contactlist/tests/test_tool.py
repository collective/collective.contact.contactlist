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
from collective.contact.contactlist.api import get_tool
from collective.contact.contactlist.vocabularies import MyListsVocabulary,\
    ListsVocabulary, CREATE_NEW_KEY


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

        adapter = get_tool()
        self.assertEqual(adapter.get_lists(), [list_1, list_2])

        self.assertEqual(adapter.get_my_lists(), [list_2])

        self.assertEqual(adapter.get_editable_lists(), [list_1, list_2])

        url = self.portal.unrestrictedTraverse('@@contactlist.mylists-url')()
        self.assertEqual(url, "http://nohost/plone/Members/testuser")

    def test_vocabularies(self):

        portal = self.portal
        directory = portal.mydirectory
        login(portal, TEST_USER_NAME)
        contacts = [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb]
        create_list("Corpses", "Description of my list", contacts)

        login(portal, 'testuser')
        contacts = [directory.armeedeterre.corpsa.divisionalpha,
                    directory.armeedeterre.corpsb]
        create_list("Divisions", "Description of my list", contacts)

        my_lists_vocabulary = getUtility(IVocabularyFactory,
                                         name=MyListsVocabulary.name)(portal)
        self.assertEqual(len(my_lists_vocabulary._terms), 1)

        lists_vocabulary = getUtility(IVocabularyFactory,
                                         name=ListsVocabulary.name)(portal)
        self.assertEqual(len(lists_vocabulary._terms), 2)
        self.assertEqual(lists_vocabulary._terms[0].title, "Divisions")
        self.assertEqual(lists_vocabulary._terms[1].title, "Corpses (%s)" % TEST_USER_ID)

    def test_views(self):
        portal = self.portal
        login(portal, 'testuser')
        self.assertFalse(portal.restrictedTraverse('@@contactlist.can-add-to-list')())
        self.assertTrue(portal.mydirectory.armeedeterre.restrictedTraverse('@@contactlist.can-add-to-list')())

        addview = portal.restrictedTraverse('@@contactlist.add-to-list')
        addview.request['REQUEST_METHOD'] = 'POST'
        addview.request['form.widgets.contact_list'] = CREATE_NEW_KEY
        addview.request['form.widgets.title'] = u"My new list"
        addview.request['form.widgets.description'] = u"My new list"
        addview.request['form.widgets.contacts'] = ['/plone/mydirectory/armeedeterre/corpsa']
        addview.update()
        addview.form_instance.applySave(addview.form_instance, None)
        self.assertIn('my-new-list', portal.Members.testuser)
        new_list = portal.Members.testuser['my-new-list']
        self.assertEqual(get_contacts(new_list),
                         [portal.mydirectory.armeedeterre.corpsa])

        addview.request['form.widgets.contact_list'] = new_list.UID()
        addview.request['form.widgets.contacts'] = ['/plone/mydirectory/armeedeterre/corpsb']
        addview.update()
        addview.form_instance.applySave(addview.form_instance, None)
        self.assertEqual(set(get_contacts(new_list)),
                         set([portal.mydirectory.armeedeterre.corpsa,
                              portal.mydirectory.armeedeterre.corpsb]))


        replaceview = portal.restrictedTraverse('@@contactlist.replace-list')
        replaceview.request['form.widgets.contact_list'] = new_list.UID()
        replaceview.request['form.widgets.contacts'] = ['/plone/mydirectory/armeedeterre/corpsb']
        replaceview.update()
        replaceview.form_instance.applySave(replaceview.form_instance, None)
        self.assertEqual(set(get_contacts(new_list)),
                         set([portal.mydirectory.armeedeterre.corpsb]))

        removeview = new_list.restrictedTraverse('@@contactlist.remove-from-list')
        removeview.request['uids'] = [portal.mydirectory.armeedeterre.corpsb.UID()]
        removeview()
        self.assertEqual(get_contacts(new_list), [])
# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.api import extend_list
from collective.contact.contactlist.api import get_contacts
from collective.contact.contactlist.api import replace_list
from collective.contact.contactlist.api import update_list
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.testing.loggingsupport import InstalledHandler

import logging

# TODO: tests should not depend on collective.contact.core test data...


class TestApi(IntegrationTestCase):

    def setUp(self):
        super(TestApi, self).setUp()
        self.directory = self.portal.mydirectory
        login(self.portal, TEST_USER_NAME)

    def test_create_list(self):
        army = self.directory.armeedeterre
        create_list("Corpses", "Description of my list", [army.corpsa, army.corpsb])
        user_folder = self.portal.Members[TEST_USER_ID]
        self.assertIn('corpses', user_folder)
        self.assertEqual(user_folder.corpses.Description(), "Description of my list")
        self.assertListsHaveSameContents(get_contacts(user_folder.corpses), [army.corpsa, army.corpsb])
        # a user without user folder can't create a list
        login(self.portal, 'member')
        with self.assertRaises(ValueError):
            create_list("Corpses", "", [army.corpsa])

    def test_update_list(self):
        army = self.directory.armeedeterre
        contact_list = create_list("Corpses", "", [army.corpsa])
        # deprecation warning (assertLogs is Python 3 only)
        handler = InstalledHandler('collective.contact.contactlist', level=logging.WARNING)
        try:
            self.assertEqual(update_list(contact_list, [army.corpsa, army.corpsb]), [army.corpsb])
        finally:
            handler.uninstall()
        self.assertEqual([r.levelname for r in handler.records], ['WARNING'])
        self.assertListsHaveSameContents(get_contacts(contact_list), [army.corpsa, army.corpsb])

    def test_extend_list(self):
        army = self.directory.armeedeterre
        contact_list = create_list("Corpses", "", [army.corpsa, army.corpsb])
        # only new contacts are added
        self.assertEqual(extend_list(contact_list, [army.corpsa, army.corpsa.divisionalpha]),
                         [army.corpsa.divisionalpha])
        self.assertListsHaveSameContents(get_contacts(contact_list),
                                         [army.corpsa, army.corpsb, army.corpsa.divisionalpha])
        self.assertEqual(extend_list(contact_list, [army.corpsa]), [])
        # a user who can't edit the list
        login(self.portal, 'member')
        with self.assertRaises(Unauthorized):
            extend_list(contact_list, [army])

    def test_replace_list(self):
        army = self.directory.armeedeterre
        contact_list = create_list("List 1", "Description of my list", [army])
        replace_list(contact_list=contact_list, contacts=[army.corpsa, army.corpsb])
        self.assertListsHaveSameContents(get_contacts(contact_list), [army.corpsa, army.corpsb])
        # a user who can't edit the list
        login(self.portal, 'member')
        with self.assertRaises(Unauthorized):
            replace_list(contact_list, [army])
        self.assertListsHaveSameContents(get_contacts(contact_list), [army.corpsa, army.corpsb])

    def test_get_contacts(self):
        army = self.directory.armeedeterre
        list1 = create_list("List 1", "Description of my list", [army.corpsa, army])
        list2 = create_list("List 2", "Description of my list", [army.corpsa, army.corpsb])
        list3 = create_list("List 3", "Description of my list", [])

        self.assertListsHaveSameContents(get_contacts(list1, list2, operator='or'),
                                         [army, army.corpsa, army.corpsb])
        self.assertListsHaveSameContents(get_contacts(list1, list3, operator='or'), [army.corpsa, army])
        self.assertListsHaveSameContents(get_contacts(list3, list1, operator='or'), [army.corpsa, army])
        self.assertListsHaveSameContents(get_contacts(list1, list2, operator='and'), [army.corpsa])
        self.assertListsHaveSameContents(get_contacts(list1, list3, operator='and'), [])
        self.assertListsHaveSameContents(get_contacts(list1, operator='and'), [army.corpsa, army])
        self.assertListsHaveSameContents(get_contacts(list3, operator='and'), [])
        # 'or' is the default operator
        self.assertListsHaveSameContents(get_contacts(list1, list2), [army, army.corpsa, army.corpsb])
        self.assertEqual(get_contacts(), [])
        with self.assertRaises(ValueError):
            get_contacts(list1, operator='xor')
        with self.assertRaises(ValueError):
            get_contacts(list1, unknown=True)

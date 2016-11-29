# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from collective.contact.contactlist.source import ContactListSourceBinder
from plone.uuid.interfaces import IUUID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone import api
from plone.app.testing import login
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID

from collective.contact.contactlist.api import create_list, extend_list, \
    get_contacts, replace_list
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.api import get_tool
from collective.contact.contactlist.vocabularies import MyListsVocabulary, \
    ListsVocabulary, CREATE_NEW_KEY


# TODO: tests should not depend on collective.contact.core test data...

class TestTool(IntegrationTestCase):
    """Test installation of collective.contact.contactlist into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def assertListsHaveSameContents(self, contents_1, contents_2):
        self.assertEqual(sorted([c.getPhysicalPath() for c in contents_1]),
                         sorted([c.getPhysicalPath() for c in contents_2]))

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
        extend_list(user_folder.corpses, [directory.armeedeterre.corpsa,
                                          directory.armeedeterre.corpsa.divisionalpha])
        self.assertEqual(len(user_folder.corpses.contacts), 3)
        contacts = get_contacts(user_folder.corpses)
        self.assertEqual(len(contacts), 3)
        self.assertIn(directory.armeedeterre.corpsa, contacts)

    def test_get_contacts(self):
        portal = self.portal
        login(portal, TEST_USER_NAME)
        directory = portal.mydirectory
        contacts = [directory.armeedeterre.corpsa, directory.armeedeterre]
        list1 = create_list("List 1", "Description of my list", contacts)
        contacts = [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb]
        list2 = create_list("List 2", "Description of my list", contacts)
        list3 = create_list("List 3", "Description of my list", [])

        self.assertListsHaveSameContents(
            get_contacts(list1, list2, operator='or'),
            [directory.armeedeterre, directory.armeedeterre.corpsa, directory.armeedeterre.corpsb])

        self.assertListsHaveSameContents(
            get_contacts(list1, list3, operator='or'),
            [directory.armeedeterre.corpsa, directory.armeedeterre])

        self.assertListsHaveSameContents(
            get_contacts(list3, list1, operator='or'),
            [directory.armeedeterre.corpsa, directory.armeedeterre])

        self.assertListsHaveSameContents(
            get_contacts(list1, list2, operator='and'),
            [directory.armeedeterre.corpsa])

        self.assertListsHaveSameContents(
            get_contacts(list1, operator='and'),
            [directory.armeedeterre.corpsa, directory.armeedeterre])

        self.assertListsHaveSameContents(
            get_contacts(list3, operator='and'),
            [])

    def test_replace_list(self):
        portal = self.portal
        login(portal, TEST_USER_NAME)
        directory = portal.mydirectory
        list1 = create_list("List 1", "Description of my list",
                            [directory.armeedeterre])
        contacts = [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb]
        replace_list(contact_list=list1, contacts=contacts)
        self.assertListsHaveSameContents(get_contacts(list1), contacts)

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
        # the sort order is undefined
        self.assertListsHaveSameContents(adapter.get_lists(), [list_1, list_2])

        self.assertEqual(adapter.get_my_lists(), [list_2])

        self.assertListsHaveSameContents(adapter.get_editable_lists(), [list_1, list_2])

        url = self.portal.unrestrictedTraverse('@@contactlist.mylists-url')()
        self.assertEqual(url, "http://nohost/plone/Members/testuser")

        self.assertListsHaveSameContents(
            adapter.get_lists_for_contact(directory.armeedeterre.corpsb),
            [list_1, list_2])

        self.assertListsHaveSameContents(
            adapter.get_lists_for_contact(directory.armeedeterre.corpsa),
            [list_1])

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

    def test_source(self):
        def assertTermsMatchContents(contents_1, contents_2):
            self.assertEqual(sorted([c.token for c in contents_1]),
                             sorted(['/'.join(c.getPhysicalPath()) for c in contents_2]))

        portal = self.portal
        login(portal, 'testuser')
        directory = portal.mydirectory
        create_list("Corpses", "Description of my list",
                    [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb],
                    Subject=["test-subject"])
        create_list("Corpses 2", "Description of my list", [directory.armeedeterre.corpsb],
                    Subject=["test-subject"])
        create_list("Divisions", "Description of my list",
                    [directory.armeedeterre.corpsa.divisionalpha, directory.armeedeterre.corpsa.divisionbeta],
                    Subject=["test-subject-2"])

        # or operator works
        source = ContactListSourceBinder(contact_lists_query={'Subject': 'test-subject'},
                                         contact_lists_operator='or',
                                         portal_type='organization')(portal)
        assertTermsMatchContents(source.search(''),
                                 [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb])

        # and operator works
        source = ContactListSourceBinder(contact_lists_query={'Subject': 'test-subject'},
                                         contact_lists_operator='and',
                                         portal_type='organization')(portal)
        assertTermsMatchContents(source.search(''),
                                 [directory.armeedeterre.corpsb])

        # combines well with content filter
        source = ContactListSourceBinder(contact_lists_query={'id': 'corpses'}, getId='corpsb')(portal)
        assertTermsMatchContents(source.search(''),
                                 [directory.armeedeterre.corpsb])

        # combines well with specific query filter
        source = ContactListSourceBinder(contact_lists_query={'Subject': 'test-subject'},
                                         contact_lists_operator='or',
                                         portal_type='organization')(portal)
        assertTermsMatchContents(source.search('path:/mydirectory/armeedeterre/corpsb'),
                                 [directory.armeedeterre.corpsb])

        # works without content filter
        source = ContactListSourceBinder(contact_lists_query={'id': 'corpses-2'},
                                         )(portal)
        assertTermsMatchContents(source.search(''),
                                 [directory.armeedeterre.corpsb])

    def test_eea_widget(self):
        from collective.contact.contactlist.browser.eeawidget.widget import Widget
        portal = self.portal
        login(portal, 'testuser')
        directory = portal.mydirectory
        mylist = create_list("Corpses", "Description of my list",
                             [directory.armeedeterre.corpsa, directory.armeedeterre.corpsb]
                             )
        mylist2 = create_list("Corpses", "Description of my list",
                              [directory.armeedeterre, directory.armeedeterre.corpsb]
                              )

        class FakeData(object):
            hidden = False

            def __init__(self, data):
                self.data = data

            def getId(self):
                return 'contact_lists'

            def get(self, val, default=None):
                return self.data.get(val, default)

        class FakeRequest(object):
            debug = False

        widget = Widget(self.portal, FakeRequest(), data=FakeData({'index': 'UID'}))

        form = {'contact_lists': [IUUID(mylist)]}
        query = widget.query(form=form)
        self.assertItemsEqual(query['UID'], [
            IUUID(directory.armeedeterre.corpsa),
            IUUID(directory.armeedeterre.corpsb)
        ])

        # check empty cases
        form = {'contact_lists': []}
        query = widget.query(form=form)
        self.assertEqual(query, {})

        form = {'contact_lists': None}
        query = widget.query(form=form)
        self.assertEqual(query, {})

        form = {}
        query = widget.query(form=form)
        self.assertEqual(query, {})

        # or operator
        form = {'contact_lists': [IUUID(mylist), IUUID(mylist2)]}
        query = widget.query(form=form)
        self.assertItemsEqual(query['UID'], [
            IUUID(directory.armeedeterre),
            IUUID(directory.armeedeterre.corpsa),
            IUUID(directory.armeedeterre.corpsb),
        ])

        # and operator
        widget = Widget(self.portal, FakeRequest(),
                        data=FakeData({'index': 'UID', 'operator': 'and'}))
        form = {'contact_lists': [IUUID(mylist), IUUID(mylist2)]}
        query = widget.query(form=form)
        self.assertItemsEqual(query['UID'], [
            IUUID(directory.armeedeterre.corpsb)]
                         )

        form = {'contact_lists': [IUUID(mylist)]}
        query = widget.query(form=form)
        self.assertItemsEqual(query['UID'], [
            IUUID(directory.armeedeterre.corpsa),
            IUUID(directory.armeedeterre.corpsb)]
                         )

        widget = Widget(self.portal, FakeRequest(),
                        data=FakeData({'index': 'UID',
                                       'vocabulary': 'collective.contact.contactlist.lists'
                                       }))
        count = widget.count(api.content.find(portal_type='organization'))
        self.assertEqual(count, {
            IUUID(mylist): 2,
            IUUID(mylist2): 2,
            '': 7,
            'all': 7
        })

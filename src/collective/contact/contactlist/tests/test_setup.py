# -*- coding: utf-8 -*-
"""Tests of the default and uninstall profiles."""
from collective.contact.contactlist.interfaces import ICollectiveContactContactlistLayer
from collective.contact.contactlist.testing import IntegrationTestCase
from plone import api
from plone.base.utils import get_installer
from plone.browserlayer import utils
from plone.dexterity.browser.add import DefaultAddView

BUNDLE_RECORD = 'plone.bundles/collective-contact-contactlist.jscompilation'
ICON_RECORD = 'plone.icon.contenttype/contact_list'


class TestSetup(IntegrationTestCase):

    def setUp(self):
        super(TestSetup, self).setUp()
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_install(self):
        self.assertTrue(self.installer.is_product_installed('collective.contact.contactlist'))
        self.assertIn(ICollectiveContactContactlistLayer, utils.registered_layers())
        # registry.xml
        self.assertEqual(api.portal.get_registry_record(BUNDLE_RECORD),
                         '++resource++collective.contact.contactlist/javascript.js')
        self.assertEqual(api.portal.get_registry_record(ICON_RECORD),
                         '++plone++bootstrap-icons/person-lines-fill.svg')
        self.assertTrue(api.portal.get_registry_record('plone.enable_user_folders'))
        self.assertTrue(api.portal.get_tool('portal_membership').memberareaCreationFlag)
        # actions.xml
        actions = api.portal.get_tool('portal_actions')
        add_to_list = actions.object_buttons['contactlist-addtolist']
        self.assertIn("ajax_load=1", add_to_list.url_expr)
        self.assertEqual(add_to_list.modal, '{"actionOptions": {"displayInModal": false}}')
        self.assertIn('contact-contactlist-mylists', actions.user)
        # types/contact_list.xml
        fti = api.portal.get_tool('portal_types')['contact_list']
        self.assertEqual(fti.icon_expr, 'string:contenttype/contact_list')
        add_view = self.portal.Members.testuser.restrictedTraverse('++add++contact_list')
        self.assertIsInstance(add_view, DefaultAddView)

    def test_uninstall(self):
        self.installer.uninstall_product('collective.contact.contactlist')
        self.assertFalse(self.installer.is_product_installed('collective.contact.contactlist'))
        self.assertNotIn(ICollectiveContactContactlistLayer, utils.registered_layers())
        self.assertIsNone(api.portal.get_registry_record(BUNDLE_RECORD, default=None))
        self.assertIsNone(api.portal.get_registry_record(ICON_RECORD, default=None))
        actions = api.portal.get_tool('portal_actions')
        self.assertNotIn('contactlist-addtolist', actions.object_buttons)
        self.assertNotIn('contact-contactlist-mylists', actions.user)

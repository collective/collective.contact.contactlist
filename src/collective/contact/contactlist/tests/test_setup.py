"""Tests of the default and uninstall profiles."""

from collective.contact.contactlist.interfaces import ICollectiveContactContactlistLayer
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.testing import PLONE_MAJOR
from plone import api
from plone.browserlayer import utils
from plone.dexterity.browser.add import DefaultAddView

import unittest

try:
    from plone.base.utils import get_installer
except ImportError:  # Plone 4: portal_quickinstaller
    get_installer = None

PRODUCT = "collective.contact.contactlist"
JAVASCRIPT = "++resource++collective.contact.contactlist/javascript.js"
BUNDLE_RECORD = "plone.bundles/collective-contact-contactlist.jscompilation"
ICON_RECORD = "plone.icon.contenttype/contact_list"


class TestSetup(IntegrationTestCase):

    def is_installed(self):
        if get_installer is None:
            return api.portal.get_tool("portal_quickinstaller").isProductInstalled(
                PRODUCT
            )
        return get_installer(self.portal, self.layer["request"]).is_product_installed(
            PRODUCT
        )

    def uninstall(self):
        if get_installer is None:
            api.portal.get_tool("portal_quickinstaller").uninstallProducts([PRODUCT])
        else:
            get_installer(self.portal, self.layer["request"]).uninstall_product(PRODUCT)

    def test_install(self):
        self.assertTrue(self.is_installed())
        self.assertIn(ICollectiveContactContactlistLayer, utils.registered_layers())
        self.assertTrue(api.portal.get_tool("portal_membership").memberareaCreationFlag)
        actions = api.portal.get_tool("portal_actions")
        add_to_list = actions.object_buttons["contactlist-addtolist"]
        self.assertIn(
            "/@@contactlist.add-to-list?form.widgets.contacts:list=",
            add_to_list.url_expr,
        )
        self.assertIn("contact-contactlist-mylists", actions.user)
        fti = api.portal.get_tool("portal_types")["contact_list"]
        add_view = self.portal.Members.testuser.restrictedTraverse(
            "++add++contact_list"
        )
        self.assertIsInstance(add_view, DefaultAddView)
        if PLONE_MAJOR < 5:
            # jsregistry.xml: the javascript opens the "Add to list" action in an overlay
            self.assertIn(
                JAVASCRIPT, api.portal.get_tool("portal_javascripts").getResourceIds()
            )
            # skin image of collective.contact.core
            self.assertEqual(fti.icon_expr, "string:${portal_url}/directory_icon.png")
        else:
            # registry.xml
            self.assertEqual(api.portal.get_registry_record(BUNDLE_RECORD), JAVASCRIPT)
            self.assertEqual(
                api.portal.get_registry_record(ICON_RECORD),
                "++plone++bootstrap-icons/person-lines-fill.svg",
            )
            self.assertTrue(api.portal.get_registry_record("plone.enable_user_folders"))
            # actions.xml: the "Add to list" action opens in a modal
            self.assertIn("ajax_load=1", add_to_list.url_expr)
            self.assertEqual(
                add_to_list.modal, '{"actionOptions": {"displayInModal": false}}'
            )
            self.assertEqual(fti.icon_expr, "string:contenttype/contact_list")

    @unittest.skipIf(
        PLONE_MAJOR < 5,
        "bundles are Plone 5+: Plone 4 registers the script in portal_javascripts "
        "(checked in test_install)",
    )
    def test_bundle(self):
        # classic script, only used at click time: no dependency on eea.facetednavigation's (optional) bundles
        bundle = "plone.bundles/collective-contact-contactlist"
        self.assertEqual(api.portal.get_registry_record(bundle + ".depends"), "plone")
        self.assertTrue(api.portal.get_registry_record(bundle + ".load_defer"))
        self.assertFalse(api.portal.get_registry_record(bundle + ".load_async"))

    def test_uninstall(self):
        self.uninstall()
        self.assertFalse(self.is_installed())
        self.assertNotIn(ICollectiveContactContactlistLayer, utils.registered_layers())
        actions = api.portal.get_tool("portal_actions")
        self.assertNotIn("contactlist-addtolist", actions.object_buttons)
        self.assertNotIn("contact-contactlist-mylists", actions.user)
        if PLONE_MAJOR < 5:
            self.assertNotIn(
                JAVASCRIPT, api.portal.get_tool("portal_javascripts").getResourceIds()
            )
        else:
            self.assertIsNone(
                api.portal.get_registry_record(BUNDLE_RECORD, default=None)
            )
            self.assertIsNone(api.portal.get_registry_record(ICON_RECORD, default=None))

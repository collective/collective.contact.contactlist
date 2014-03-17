# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.contact.contactlist.testing import IntegrationTestCase
from plone import api


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

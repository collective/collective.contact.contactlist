# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from collective.contact.facetednav.interfaces import IActionsEnabled
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import zope
from zope.interface import alsoProvides

import collective.contact.contactlist
import collective.contact.core
import collective.contact.facetednav
import collective.excelexport
import collective.js.backbone
import os
import transaction
import unittest


class CollectiveContactContactlistLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    products = ('collective.contact.contactlist',
               )

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=collective.contact.contactlist,
                      name='testing.zcml')
        zope.installProduct(app, 'collective.contact.contactlist')
        self.loadZCML(package=collective.contact.core,
                      name='testing.zcml')
        for p in self.products:
            zope.installProduct(app, p)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.contact.core:testing')
        # insert some test data
        applyProfile(portal, 'collective.contact.core:test_data')
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.contact.contactlist:testing')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        api.user.create(email='testuser@example.com',
                        username='testuser',
                        password='testuser1',
                        roles=['Manager'],
                        properties={'fullname': 'Test user'})
        # plain member without user folder
        api.user.create(email='member@example.com', username='member', password='member123')
        login(portal, TEST_USER_NAME)
        folder_id = portal.invokeFactory('Folder', 'folder')
        portal[folder_id].reindexObject()
        members = portal.Members
        api.content.create(container=members, type='Folder', id=TEST_USER_ID)
        api.content.create(container=members, type='Folder', id='testuser')

        # Commit so that the test browser sees these objects
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            zope.uninstallProduct(app, p)


FIXTURE = CollectiveContactContactlistLayer(
    name="FIXTURE"
    )


INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="INTEGRATION"
    )


FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="FUNCTIONAL"
    )


ACCEPTANCE = FunctionalTesting(bases=(FIXTURE,
                                      REMOTE_LIBRARY_BUNDLE_FIXTURE,
                                      zope.WSGI_SERVER_FIXTURE),
                               name="ACCEPTANCE")


class CollectiveContactContactlistAddonsLayer(PloneSandboxLayer):
    """Optional integrations: contacts faceted navigation and excel export"""

    defaultBases = (FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # dependency of the facetednav profile, loaded by z3c.autoinclude in an instance
        self.loadZCML(package=collective.js.backbone)
        self.loadZCML(package=collective.contact.facetednav)
        self.loadZCML(package=collective.excelexport)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.contact.facetednav:default')
        directory = portal.mydirectory
        alsoProvides(directory, IFacetedNavigable, IActionsEnabled)
        with open(os.path.join(os.path.dirname(__file__), 'tests', 'contacts-faceted.xml'), 'rb') as xml:
            directory.unrestrictedTraverse('@@faceted_exportimport')._import_xml(import_file=xml)
        directory.reindexObject()
        transaction.commit()


ADDONS_FIXTURE = CollectiveContactContactlistAddonsLayer(
    name="ADDONS_FIXTURE"
    )


ADDONS_ACCEPTANCE = FunctionalTesting(bases=(ADDONS_FIXTURE,
                                             REMOTE_LIBRARY_BUNDLE_FIXTURE,
                                             zope.WSGI_SERVER_FIXTURE),
                                      name="ADDONS_ACCEPTANCE")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']

    def assertListsHaveSameContents(self, contents_1, contents_2):
        self.assertEqual(sorted([c.getPhysicalPath() for c in contents_1]),
                         sorted([c.getPhysicalPath() for c in contents_2]))


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL

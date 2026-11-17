"""Base module for unittesting (Plone 4.3 and Plone 6)."""

from collective.contact.facetednav.interfaces import IActionsEnabled
from eea.facetednavigation.interfaces import IDisableSmartFacets
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from plone import api
from plone.app.robotframework.content import Content
from plone.app.robotframework.remote import RemoteLibraryLayer
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
from Products.CMFPlone.utils import getFSVersionTuple
from zope.globalrequest import clearRequest
from zope.globalrequest import getRequest
from zope.globalrequest import setLocal
from zope.interface import alsoProvides

import collective.contact.contactlist
import collective.contact.core
import collective.contact.facetednav
import collective.excelexport
import os
import transaction
import unittest

try:
    from plone.testing.zope import installProduct
    from plone.testing.zope import uninstallProduct
    from plone.testing.zope import WSGI_SERVER_FIXTURE as SERVER_FIXTURE
except ImportError:  # Plone 4
    from plone.testing.z2 import installProduct
    from plone.testing.z2 import uninstallProduct
    from plone.testing.z2 import ZSERVER_FIXTURE as SERVER_FIXTURE

try:  # Plone 5+: automatic CSRF check of plone.protect
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:  # Plone 4
    IDisableCSRFProtection = None

try:  # dependency of the collective.contact.facetednav profile on Plone 4, dropped on Plone 6
    import collective.js.backbone as backbone
except ImportError:
    backbone = None


PLONE_MAJOR = getFSVersionTuple()[0]

# a test pinning a bug of the Plone 4 code, fixed by the Plone 6 migration (see MIGRATION.md)
expectedFailureOnPlone4 = (
    unittest.expectedFailure if PLONE_MAJOR < 5 else (lambda func: func)
)


class CollectiveContactContactlistLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    products = ("collective.contact.contactlist",)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=collective.contact.contactlist, name="testing.zcml")
        installProduct(app, "collective.contact.contactlist")
        self.loadZCML(package=collective.contact.core, name="testing.zcml")
        for p in self.products:
            installProduct(app, p)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        setLocal(
            "request", portal.REQUEST
        )  # collective.fingerpointing (imio.fpaudit) needs a request
        # Install into Plone site using portal_setup
        applyProfile(portal, "collective.contact.core:testing")
        # insert some test data
        applyProfile(portal, "collective.contact.core:test_data")
        # Install into Plone site using portal_setup
        applyProfile(portal, "collective.contact.contactlist:testing")
        if PLONE_MAJOR < 5:
            # javascript of the collective.contact.widget autocomplete, installed on a Plone 4 site
            applyProfile(portal, "plone.formwidget.contenttree:default")

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ["Manager"])
        api.user.create(
            email="testuser@example.com",
            username="testuser",
            password="testuser1",
            roles=["Manager"],
            properties={"fullname": "Test user"},
        )
        # plain member without user folder
        api.user.create(
            email="member@example.com", username="member", password="member123"
        )
        login(portal, TEST_USER_NAME)
        folder_id = portal.invokeFactory("Folder", "folder")
        portal[folder_id].reindexObject()
        if "Members" not in portal:
            # Plone 4 creates it with the site content (plone-content profile), not in PLONE_FIXTURE;
            # Plone 6: the package creates it on install
            api.content.create(container=portal, type="Folder", id="Members")
        members = portal.Members
        api.content.create(container=members, type="Folder", id=TEST_USER_ID)
        api.content.create(container=members, type="Folder", id="testuser")

        # Commit so that the test browser sees these objects
        transaction.commit()
        clearRequest()  # else the next layers get a request bound to a closed connection

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            uninstallProduct(app, p)


FIXTURE = CollectiveContactContactlistLayer(name="FIXTURE")


INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="INTEGRATION")


FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="FUNCTIONAL")


class CSRFSafeContent(Content):
    """Set field value aborted by plone.protect otherwise (plone.app.robotframework 3.0.0 disables
    the CSRF check in Create content, not here)"""

    def set_field_value(self, uid, field, value, field_type):
        """Set field value with a specific type"""
        if IDisableCSRFProtection is not None:
            alsoProvides(getRequest(), IDisableCSRFProtection)
        return super().set_field_value(uid, field, value, field_type)


REMOTE_LIBRARY_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE,),
    libraries=tuple(
        CSRFSafeContent if lib is Content else lib
        for lib in REMOTE_LIBRARY_BUNDLE_FIXTURE.libraryBases[1:]
    ),
    name="RemoteLibraryBundle:RobotRemote",
)


ACCEPTANCE = FunctionalTesting(
    bases=(FIXTURE, REMOTE_LIBRARY_FIXTURE, SERVER_FIXTURE), name="ACCEPTANCE"
)


class CollectiveContactContactlistAddonsLayer(PloneSandboxLayer):
    """Optional integrations: contacts faceted navigation and excel export"""

    defaultBases = (FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # dependency of the facetednav profile, loaded by z3c.autoinclude in an instance
        if backbone is not None:
            self.loadZCML(package=backbone)
        self.loadZCML(package=collective.contact.facetednav)
        self.loadZCML(package=collective.excelexport)

    def setUpPloneSite(self, portal):
        setLocal(
            "request", portal.REQUEST
        )  # collective.fingerpointing (imio.fpaudit) needs a request
        applyProfile(portal, "collective.contact.facetednav:default")
        directory = portal.mydirectory
        # smart facets hide the criteria when the results have no pagination
        alsoProvides(directory, IFacetedNavigable, IActionsEnabled, IDisableSmartFacets)
        with open(
            os.path.join(os.path.dirname(__file__), "tests", "contacts-faceted.xml"),
            "rb",
        ) as xml:
            directory.unrestrictedTraverse("@@faceted_exportimport")._import_xml(
                import_file=xml
            )
        directory.reindexObject()
        transaction.commit()
        clearRequest()


ADDONS_FIXTURE = CollectiveContactContactlistAddonsLayer(name="ADDONS_FIXTURE")


ADDONS_ACCEPTANCE = FunctionalTesting(
    bases=(ADDONS_FIXTURE, REMOTE_LIBRARY_FIXTURE, SERVER_FIXTURE),
    name="ADDONS_ACCEPTANCE",
)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super().setUp()
        self.portal = self.layer["portal"]

    def assertListsHaveSameContents(self, contents_1, contents_2):
        self.assertEqual(
            sorted([c.getPhysicalPath() for c in contents_1]),
            sorted([c.getPhysicalPath() for c in contents_2]),
        )


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL

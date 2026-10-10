# -*- coding: utf-8 -*-
from collective.contact.contactlist.browser.facetednav import AddToListAction
from collective.contact.contactlist.browser.facetednav import ReplaceListAction
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login


class TestBatchActions(IntegrationTestCase):
    """Buttons of the collective.contact.facetednav batch actions, wired to javascript.js"""

    def setUp(self):
        super(TestBatchActions, self).setUp()
        self.directory = self.portal.mydirectory
        self.request = self.layer["request"]

    def test_available(self):
        login(self.portal, "testuser")
        self.assertTrue(AddToListAction(self.directory, self.request, None, None).available())
        self.assertTrue(ReplaceListAction(self.directory, self.request, None, None).available())
        # without user folder, no list
        login(self.portal, "member")
        self.assertFalse(AddToListAction(self.directory, self.request, None, None).available())
        self.assertFalse(ReplaceListAction(self.directory, self.request, None, None).available())

    def test_render(self):
        login(self.portal, "testuser")
        html = AddToListAction(self.directory, self.request, None, None).render()
        self.assertIn('id="contact-facetednav-action-addtolist"', html)
        self.assertIn('onclick="contactcontactlist.facetednav_addtolist()"', html)
        html = ReplaceListAction(self.directory, self.request, None, None).render()
        self.assertIn('id="contact-facetednav-action-replace"', html)
        self.assertIn('onclick="contactcontactlist.facetednav_replacelist()"', html)

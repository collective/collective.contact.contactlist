# -*- coding: utf-8 -*-
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login


class TestMyListsURL(IntegrationTestCase):

    def test_call(self):
        login(self.portal, "testuser")
        view = self.portal.unrestrictedTraverse("@@contactlist.mylists-url")
        self.assertEqual(view(), "http://nohost/plone/Members/testuser")
        # a user without user folder: the "My contact lists" action is hidden
        login(self.portal, "member")
        view = self.portal.unrestrictedTraverse("@@contactlist.mylists-url")
        self.assertEqual(view(), "")

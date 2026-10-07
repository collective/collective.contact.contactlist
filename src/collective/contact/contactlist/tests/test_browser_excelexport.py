# -*- coding: utf-8 -*-
from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.browser.excelexport import ExportLinkViewlet
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login


class TestExportLinkViewlet(IntegrationTestCase):

    def test_render(self):
        login(self.portal, 'testuser')
        contact_list = create_list("Exported", "", [self.portal.mydirectory.armeedeterre])
        viewlet = ExportLinkViewlet(contact_list, self.layer['request'], None)
        viewlet.update()
        html = viewlet.render()
        self.assertIn('href="http://nohost/plone/Members/testuser/exported/@@collective.excelexport"', html)
        # the xls.png image of Plone 4 doesn't exist anymore
        self.assertIn('src="http://nohost/plone/++plone++', html)

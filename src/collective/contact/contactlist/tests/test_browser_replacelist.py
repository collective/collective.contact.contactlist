# -*- coding: utf-8 -*-
from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.api import get_contacts
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login


class TestReplaceListForm(IntegrationTestCase):

    def test_applySave(self):
        portal = self.portal
        army = portal.mydirectory.armeedeterre
        login(portal, 'testuser')
        contact_list = create_list("My list", "", [army.corpsa, army.corpsb])
        replaceview = portal.restrictedTraverse('@@contactlist.replace-list')
        replaceview.request['REQUEST_METHOD'] = 'POST'
        replaceview.request['form.widgets.contact_list'] = contact_list.UID()
        replaceview.request['form.widgets.contacts'] = ['/plone/mydirectory/armeedeterre/corpsb']
        replaceview.update()
        replaceview.form_instance.applySave(replaceview.form_instance, None)
        self.assertEqual(get_contacts(contact_list), [army.corpsb])

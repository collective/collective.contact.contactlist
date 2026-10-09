# -*- coding: utf-8 -*-
from collective.contact.contactlist.api import get_contacts
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.vocabularies import CREATE_NEW_KEY
from plone.app.testing import login
from plone.protect.authenticator import createToken
from z3c.form.interfaces import HIDDEN_MODE
from zExceptions import Forbidden


class TestAddToListForm(IntegrationTestCase):

    def test_updateWidgets(self):
        # opened by the "Add to list" action: GET request with the contact, in a modal
        login(self.portal, 'testuser')
        request = self.layer['request']
        request['REQUEST_METHOD'] = 'GET'
        request.form['form.widgets.contacts'] = ['/plone/mydirectory/armeedeterre']
        request.form['ajax_load'] = '1'
        addview = self.portal.restrictedTraverse('@@contactlist.add-to-list')
        addview.update()
        widget = addview.form_instance.widgets['contacts']
        self.assertEqual(widget.mode, HIDDEN_MODE)
        self.assertIn('value="/plone/mydirectory/armeedeterre"', widget.render())

    def test_applySave(self):
        portal = self.portal
        army = portal.mydirectory.armeedeterre
        login(portal, 'testuser')
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
        self.assertEqual(get_contacts(new_list), [army.corpsa])

        addview.request['form.widgets.contact_list'] = new_list.UID()
        addview.request['form.widgets.contacts'] = ['/plone/mydirectory/armeedeterre/corpsb']
        addview.update()
        addview.form_instance.applySave(addview.form_instance, None)
        self.assertEqual(set(get_contacts(new_list)), set([army.corpsa, army.corpsb]))

    def test_csrf(self):
        # the modal form (ajax_load) has the token, the Save button needs it
        login(self.portal, 'testuser')
        request = self.layer['request']
        request.form['ajax_load'] = '1'
        addview = self.portal.restrictedTraverse('@@contactlist.add-to-list')
        addview.update()
        html = addview.form_instance.render()
        self.assertIn('name="_authenticator"', html)
        # javascript.js adds the contacts selected in the faceted navigation there
        self.assertIn('id="formfield-form-widgets-contacts"', html)
        request['REQUEST_METHOD'] = 'POST'
        request.form.update({'form.widgets.contact_list': CREATE_NEW_KEY,
                             'form.widgets.title': u"My new list",
                             'form.widgets.contacts': ['/plone/mydirectory/armeedeterre'],
                             'form.buttons.save': u"Save"})
        addview = self.portal.restrictedTraverse('@@contactlist.add-to-list')
        self.assertRaises(Forbidden, addview.update)
        self.assertNotIn('my-new-list', self.portal.Members.testuser)
        request.form['_authenticator'] = createToken()
        addview = self.portal.restrictedTraverse('@@contactlist.add-to-list')
        addview.update()
        self.assertIn('my-new-list', self.portal.Members.testuser)


class TestCanAddToList(IntegrationTestCase):

    def test_call(self):
        portal = self.portal
        login(portal, 'testuser')
        self.assertFalse(portal.restrictedTraverse('@@contactlist.can-add-to-list')())
        self.assertTrue(portal.mydirectory.armeedeterre.restrictedTraverse('@@contactlist.can-add-to-list')())

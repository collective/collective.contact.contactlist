# -*- coding: utf-8 -*-
from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.api import get_contacts
from collective.contact.contactlist.testing import expectedFailureOnPlone4
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.vocabularies import CREATE_NEW_KEY
from plone.app.testing import login
from plone.protect.authenticator import createToken
from z3c.form.interfaces import HIDDEN_MODE
from zExceptions import Forbidden


class TestAddToListForm(IntegrationTestCase):

    # Plone 4.3.11+ (PloneHotfix20160830) ignores GET values on a POST form: the contact is lost
    @expectedFailureOnPlone4
    def test_updateWidgets(self):
        # opened by the "Add to list" action: GET request with the contact, in a modal
        login(self.portal, "testuser")
        request = self.layer["request"]
        request["REQUEST_METHOD"] = "GET"
        request.form["form.widgets.contacts"] = ["/plone/mydirectory/armeedeterre"]
        request.form["ajax_load"] = "1"
        addview = self.portal.restrictedTraverse("@@contactlist.add-to-list")
        addview.update()
        widget = addview.form_instance.widgets["contacts"]
        self.assertEqual(widget.mode, HIDDEN_MODE)
        self.assertIn('value="/plone/mydirectory/armeedeterre"', widget.render())

    def extract_errors(self, contact_list):
        # z3c.form reads request.get(): request.other (values of the previous update) before request.form
        request = self.layer["request"]
        request["REQUEST_METHOD"] = "POST"
        request["form.widgets.contact_list"] = contact_list
        request["form.widgets.contacts"] = ["/plone/mydirectory/armeedeterre"]
        addview = self.portal.restrictedTraverse("@@contactlist.add-to-list")
        addview.update()
        return [error.message for error in addview.form_instance.extractData()[1]]

    def test_checkNewListTitle(self):
        login(self.portal, "testuser")
        self.assertEqual(self.extract_errors(CREATE_NEW_KEY), ["Title of the new list is required"])
        # an existing list doesn't need a title
        self.assertEqual(self.extract_errors(create_list("Existing", "", []).UID()), [])

    def test_applySave(self):
        portal = self.portal
        army = portal.mydirectory.armeedeterre
        login(portal, "testuser")
        addview = portal.restrictedTraverse("@@contactlist.add-to-list")
        addview.request["REQUEST_METHOD"] = "POST"
        addview.request["form.widgets.contact_list"] = CREATE_NEW_KEY
        addview.request["form.widgets.title"] = "My new list"
        addview.request["form.widgets.description"] = "My new list"
        addview.request["form.widgets.contacts"] = ["/plone/mydirectory/armeedeterre/corpsa"]
        addview.update()
        addview.form_instance.applySave(addview.form_instance, None)
        self.assertIn("my-new-list", portal.Members.testuser)
        new_list = portal.Members.testuser["my-new-list"]
        self.assertEqual(get_contacts(new_list), [army.corpsa])

        addview.request["form.widgets.contact_list"] = new_list.UID()
        addview.request["form.widgets.contacts"] = ["/plone/mydirectory/armeedeterre/corpsb"]
        addview.update()
        addview.form_instance.applySave(addview.form_instance, None)
        self.assertEqual(set(get_contacts(new_list)), set([army.corpsa, army.corpsb]))

    # the Plone 4 forms don't check the CSRF token (no enableCSRFProtection, no auto CSRF in plone.protect 2)
    @expectedFailureOnPlone4
    def test_csrf(self):
        # the modal form (ajax_load) has the token, the Save button needs it
        login(self.portal, "testuser")
        request = self.layer["request"]
        request.form["ajax_load"] = "1"
        addview = self.portal.restrictedTraverse("@@contactlist.add-to-list")
        addview.update()
        html = addview.form_instance.render()
        self.assertIn('name="_authenticator"', html)
        # javascript.js adds the contacts selected in the faceted navigation there
        self.assertIn('id="formfield-form-widgets-contacts"', html)
        request["REQUEST_METHOD"] = "POST"
        request.form.update(
            {
                "form.widgets.contact_list": CREATE_NEW_KEY,
                "form.widgets.title": "My new list",
                "form.widgets.contacts": ["/plone/mydirectory/armeedeterre"],
                "form.buttons.save": "Save",
            }
        )
        addview = self.portal.restrictedTraverse("@@contactlist.add-to-list")
        self.assertRaises(Forbidden, addview.update)
        self.assertNotIn("my-new-list", self.portal.Members.testuser)
        request.form["_authenticator"] = createToken()
        addview = self.portal.restrictedTraverse("@@contactlist.add-to-list")
        addview.update()
        self.assertIn("my-new-list", self.portal.Members.testuser)


class TestCanAddToList(IntegrationTestCase):

    def test_call(self):
        portal = self.portal
        login(portal, "testuser")
        self.assertFalse(portal.restrictedTraverse("@@contactlist.can-add-to-list")())
        self.assertTrue(portal.mydirectory.armeedeterre.restrictedTraverse("@@contactlist.can-add-to-list")())

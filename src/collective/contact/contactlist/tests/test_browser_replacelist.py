from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.api import get_contacts
from collective.contact.contactlist.testing import expectedFailureOnPlone4
from collective.contact.contactlist.testing import IntegrationTestCase
from plone.app.testing import login
from plone.protect.authenticator import createToken
from zExceptions import Forbidden


class TestReplaceListForm(IntegrationTestCase):

    def test_applySave(self):
        portal = self.portal
        army = portal.mydirectory.armeedeterre
        login(portal, "testuser")
        contact_list = create_list("My list", "", [army.corpsa, army.corpsb])
        replaceview = portal.restrictedTraverse("@@contactlist.replace-list")
        replaceview.request["REQUEST_METHOD"] = "POST"
        replaceview.request["form.widgets.contact_list"] = contact_list.UID()
        replaceview.request["form.widgets.contacts"] = [
            "/plone/mydirectory/armeedeterre/corpsb"
        ]
        replaceview.update()
        replaceview.form_instance.applySave(replaceview.form_instance, None)
        self.assertEqual(get_contacts(contact_list), [army.corpsb])

    # the Plone 4 forms don't check the CSRF token (no enableCSRFProtection, no auto CSRF in plone.protect 2)
    @expectedFailureOnPlone4
    def test_csrf(self):
        # the modal form (ajax_load) has the token, the Save button needs it
        army = self.portal.mydirectory.armeedeterre
        login(self.portal, "testuser")
        contact_list = create_list("My list", "", [army.corpsa])
        request = self.layer["request"]
        request.form["ajax_load"] = "1"
        replaceview = self.portal.restrictedTraverse("@@contactlist.replace-list")
        replaceview.update()
        html = replaceview.form_instance.render()
        self.assertIn('name="_authenticator"', html)
        # javascript.js adds the selected contacts and selects the list checked in the faceted navigation
        self.assertIn('id="formfield-form-widgets-contacts"', html)
        self.assertIn('id="form-widgets-contact_list"', html)
        request["REQUEST_METHOD"] = "POST"
        request.form.update(
            {
                "form.widgets.contact_list": contact_list.UID(),
                "form.widgets.contacts": ["/plone/mydirectory/armeedeterre/corpsb"],
                "form.buttons.save": "Save",
            }
        )
        replaceview = self.portal.restrictedTraverse("@@contactlist.replace-list")
        self.assertRaises(Forbidden, replaceview.update)
        self.assertEqual(get_contacts(contact_list), [army.corpsa])
        request.form["_authenticator"] = createToken()
        replaceview = self.portal.restrictedTraverse("@@contactlist.replace-list")
        replaceview.update()
        self.assertEqual(get_contacts(contact_list), [army.corpsb])

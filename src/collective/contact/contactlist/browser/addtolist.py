from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory

from z3c.form import form
from z3c.form import field
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE

from five import grok

from Products.statusmessages.interfaces import IStatusMessage
from plone import api as ploneapi
from plone.z3cform.layout import wrap_form
from plone.formwidget.masterselect import MasterSelectField

from collective.contact.widget import schema as contactsschema
from collective.contact.widget.interfaces import IContactContent
from collective.contact.contactlist import _, api
from collective.contact.contactlist.vocabularies import CREATE_NEW_KEY
from z3c.form.error import ErrorViewSnippet
from zope.schema._bootstrapinterfaces import InvalidValue


PMF = MessageFactory('plone')

class IAddToList(Interface):

    contact_list = MasterSelectField(
        required=True,
        title=_("List where to add selected item(s)"),
        vocabulary='collective.contact.contactlist.addtolist',
        slave_fields=(
            {'name': 'title',
             #'masterSelector': 'input[name="form.widgets.contact_list"]',
             'masterId': 'form-widgets-contact_list',
             'slaveID': '#form-widgets-title',
             'action': 'show',
             'hide_values': (CREATE_NEW_KEY,),
             'siblings': True,
            },
            {'name': 'description',
             #'masterSelector': 'input[name="form.widgets.contact_list"]',
             'masterId': 'form-widgets-contact_list',
             'slaveID': '#form-widgets-description',
             'action': 'show',
             'hide_values': (CREATE_NEW_KEY,),
             'siblings': True,
            },
            )
    )

    title = schema.TextLine(title=_(u"List title"), required=False)

    description = schema.Text(title=_(u"Description"), required=False)

    contacts = contactsschema.ContactList()

class AddToListForm(form.Form):

    fields = field.Fields(IAddToList)
    ignoreContext = True
    ignoreRequest = False
    method = 'POST'

    def updateWidgets(self):
        super(AddToListForm, self).updateWidgets()
        self.widgets['contacts'].mode = HIDDEN_MODE

    def extractData(self, setErrors=True):
        data, errors = super(AddToListForm, self).extractData(setErrors=setErrors)
        data, errors = self.checkNewListTitle(data, errors)
        return data, errors

    def checkNewListTitle(self, data, errors):
        if data['contact_list'] == CREATE_NEW_KEY and not data['title']:
            message = _("Title of the new list is required")
            errors = self.addError(errors, 'title', message)

        return data, errors

    @button.buttonAndHandler(PMF('Save'), name="save")
    def applySave(self, action):
        data, errors = self.extractData()
        if errors:
            return

        contacts = data['contacts']
        if data['contact_list'] == CREATE_NEW_KEY:
            title, description = data['title'], data['description']
            contact_list = api.create_list(title, description, contacts)
            IStatusMessage(self.request).add(
                               _('msg_new_list_added',
                                 default=u"New list added with ${num} contact(s) : ${title}",
                                 mapping={'num': len(contacts),
                                          'title': title}))
        else:
            contact_list = ploneapi.content.get(UID=data['contact_list'])
            added_contacts = api.update_list(contact_list, contacts)
            IStatusMessage(self.request).add(
                               _('msg_list_updated',
                                 default=u"${title} list updated with ${num} contact(s)",
                                 mapping={'num': len(added_contacts),
                                          'title': contact_list.Title()}))

        self.request.response.redirect(contact_list.absolute_url())

    def addError(self, errors, fieldname, message):
        error = ErrorViewSnippet(InvalidValue(fieldname),
                            self.request, self.widgets[fieldname],
                            self.fields[fieldname].field, self,
                            None)
        error.message = message
        errors += (error,)
        form.widgets[fieldname].error = error
        form.widgets.errors += (error,)
        return errors


add_to_list = wrap_form(
        AddToListForm,
        label=_(u"Add to list")
    )


class CanAddToList(grok.View):
    grok.context(Interface)

    def render(self):
        return IContactContent.providedBy(self.context)
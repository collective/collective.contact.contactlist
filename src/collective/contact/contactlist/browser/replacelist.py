from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory

from z3c.form import form
from z3c.form import field
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE

from Products.statusmessages.interfaces import IStatusMessage
from plone import api as ploneapi
from plone.protect import PostOnly
from plone.z3cform.layout import wrap_form

from collective.contact.widget import schema as contactsschema
from collective.contact.contactlist import _, api


PMF = MessageFactory('plone')

class IReplaceList(Interface):

    contact_list = schema.Choice(
        required=True,
        title=_("List to update"),
        vocabulary='collective.contact.contactlist.editablelists',
    )

    contacts = contactsschema.ContactList()


class ReplaceListForm(form.Form):

    fields = field.Fields(IReplaceList)
    ignoreContext = True
    ignoreRequest = False
    method = 'POST'

    def updateWidgets(self):
        super(ReplaceListForm, self).updateWidgets()
        if 'ajax_load' in self.request:
            self.widgets['contacts'].mode = HIDDEN_MODE

    @button.buttonAndHandler(PMF('Save'), name="save")
    def applySave(self, action):
        PostOnly(self.request)
        data, errors = self.extractData()
        if errors:
            return

        contacts = data['contacts']
        contact_list = ploneapi.content.get(UID=data['contact_list'])
        added_contacts = api.replace_list(contact_list, contacts)
        IStatusMessage(self.request).add(
                           _('msg_list_replaced',
                             default=u"${title} list contacts has been replaced by ${num} contact(s)",
                             mapping={'num': len(added_contacts),
                                      'title': contact_list.Title()}))

        self.request.response.redirect(contact_list.absolute_url())


    @button.buttonAndHandler(PMF('Cancel'), name="cancel")
    def applyCancel(self, action):
        self.request.response.redirect(self.context.absolute_url())


replace_list = wrap_form(
        ReplaceListForm,
        label=_(u"Replace list contacts"),
        description=_('help_replace_list',
                      default=u"Replace contacts of selected list with selected contacts")
    )

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from plone.uuid.interfaces import IUUID
from plone.protect import PostOnly
from collective.contact.contactlist.api import get_contacts, replace_list
from collective.contact.contactlist import _


class RemoveFromList(BrowserView):

    def __call__(self):
        PostOnly(self.request)
        uids = self.request['uids']
        old_contacts = get_contacts(self.context)
        new_contacts = [c for c in old_contacts if IUUID(c) not in uids]
        replace_list(self.context, new_contacts)
        IStatusMessage(self.request).add(_('msg_removed_from_list',
               default=u"${num} contacts have been removed from list ${title}",
               mapping={'num': len(old_contacts) - len(new_contacts),
                        'title': self.context.Title()}))
        self.request.response.redirect(self.context.absolute_url())

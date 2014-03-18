from zope.interface import Interface

from five import grok

from collective.contact.contactlist.api import get_user_lists_adapter


class MyListsURL(grok.View):
    grok.context(Interface)

    def render(self):
        adapter = get_user_lists_adapter()
        return adapter.get_container().absolute_url()

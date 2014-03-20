from zope.interface import Interface

from five import grok

from collective.contact.contactlist.api import get_user_lists_adapter


class MyListsURL(grok.View):
    grok.context(Interface)

    def render(self):
        adapter = get_user_lists_adapter()
        container = adapter.get_container()
        return container and container.absolute_url() or u""

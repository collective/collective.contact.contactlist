from collective.contact.contactlist.api import get_tool
from Products.Five.browser import BrowserView


class MyListsURL(BrowserView):

    def __call__(self):
        adapter = get_tool()
        container = adapter.get_container()
        return container and container.absolute_url() or u""

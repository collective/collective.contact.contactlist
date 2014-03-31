from collective.contact.contactlist.api import get_user_lists_adapter
from Products.Five.browser import BrowserView


class MyListsURL(BrowserView):

    def __call__(self):
        adapter = get_user_lists_adapter()
        container = adapter.get_container()
        return container and container.absolute_url() or u""

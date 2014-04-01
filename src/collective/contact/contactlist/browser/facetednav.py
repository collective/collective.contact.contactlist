from collective.contact.facetednav.browser.actions.base import BatchActionBase
from collective.contact.contactlist import _
from collective.contact.contactlist.api import get_tool


class AddToListAction(BatchActionBase):

    label = _("Add to list")
    name = 'addtolist'
    klass = 'context'
    onclick = 'contactcontactlist.facetednav_addtolist()'
    weight = 110

    def available(self):
        return get_tool().get_container() is not None


class ReplaceListAction(BatchActionBase):
    label = _("Replace list")
    name = 'replace'
    klass = 'context'
    onclick = 'contactcontactlist.facetednav_replacelist()'
    weight = 120

    def available(self):
        return get_tool().get_container() is not None
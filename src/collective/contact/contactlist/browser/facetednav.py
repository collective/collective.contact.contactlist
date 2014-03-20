from collective.contact.facetednav.browser.actions.base import BatchActionBase
from collective.contact.contactlist import _


class AddToListAction(BatchActionBase):

    label = _("Add to list")
    name = 'addtolist'
    klass = 'context'
    onclick = 'contactcontactlist.facetednav_addtolist()'

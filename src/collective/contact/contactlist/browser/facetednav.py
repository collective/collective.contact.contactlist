from collective.contact.facetednav.browser.batchactions.base import ActionBase
from collective.contact.contactlist import _


class AddToListAction(ActionBase):

    label = _("Add to list")
    name = 'addtolist'
    klass = 'context'
    onclick = 'contactcontactlist.facetednav_addtolist()'

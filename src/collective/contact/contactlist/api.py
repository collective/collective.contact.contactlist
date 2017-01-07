from AccessControl.unauthorized import Unauthorized
from zope.component import getMultiAdapter, getUtility
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import modified

from z3c.relationfield.relation import RelationValue

from plone import api as ploneapi

from collective.contact.contactlist.interfaces import IUserLists
from collective.contact.contactlist import log


def get_tool():
    """Get list storage of current user
    """
    user = ploneapi.user.get_current()
    portal = ploneapi.portal.get()
    adapter = getMultiAdapter((user, portal, portal.REQUEST),
                              IUserLists)
    return adapter


def create_list(title, description, contacts, list_type='contact_list', **kwargs):
    """Create a list of contacts
    @param title: str - The title of the list of contacts
    @param description : str - The description of the list
    @param contacts: objects - A list of contact objects
    @param list_type: str - The portal type of contact_list to create
    @return: the contact list content object
    """
    container = get_tool().get_container()
    if not container:
        raise ValueError("User has no list container : %s",
                         ploneapi.user.get_current().getId())
    intids = getUtility(IIntIds)
    contact_list = ploneapi.content.create(
        container=container,
        type=list_type,
        title=title,
        description=description,
        contacts=[RelationValue(intids.getId(obj))
                  for obj in contacts],
        **kwargs
    )
    return contact_list


def update_list(contact_list, contacts):
    log.warning("update_list function is deprecated, use extend_list instead")
    return extend_list(contact_list, contacts)


def extend_list(contact_list, contacts):
    """Add contacts to a contact list
    @param contact_list: object - The contact list object
    @param contacts: objects - A list of contact objects
    @return: objects - the list of contacts that have been actually added
    """
    _check_edit_permissions(contact_list)
    current_relations = contact_list.contacts if contact_list.contacts else []
    current_contacts = [c.to_object for c in current_relations]
    new_contacts = [c for c in contacts if c not in current_contacts]
    if len(new_contacts) > 0:
        intids = getUtility(IIntIds)
        new_relations = [RelationValue(intids.getId(obj)) for obj in new_contacts]
        contact_list.contacts = current_relations + new_relations
        modified(contact_list)
        return new_contacts
    else:
        return []


def replace_list(contact_list, contacts):
    """Replace the contacts of a contact list
    @param contact_list: object - The contact list object
    @param contacts: objects - A list of contact objects
    @return: objects - the list of contacts that have been actually added
    """
    _check_edit_permissions(contact_list)
    intids = getUtility(IIntIds)
    contact_list.contacts = [RelationValue(intids.getId(obj))
                             for obj in contacts]
    modified(contact_list)
    return contacts


def get_contacts(*contact_lists, **kwargs):
    """Get the contacts from one or many contact list(s)
    kwargs can have an 'operator' option ('and' or 'or')
    so we make union or intersection of lists
    default is 'or'
    """
    operator = kwargs.pop('operator', 'or')
    if operator not in ('and', 'or'):
        raise ValueError("Operator must be 'and' or 'or'.")
    elif len(kwargs) > 0:
        raise ValueError("Unhandled parameter(s): %s" % kwargs.keys())
    elif len(contact_lists) == 0:
        return []
    elif len(contact_lists) == 1:
        if not contact_lists[0].contacts:
            return []
        return map(lambda c: c.to_object, contact_lists[0].contacts)
    elif operator == 'or':
        contacts = set()
        for contact_list in contact_lists:
            if not contact_list.contacts:
                continue
            contacts |= set(map(lambda c: c.to_object, contact_list.contacts))
        return list(contacts)
    elif operator == 'and':
        contacts = set(map(lambda c: c.to_object, contact_lists[0].contacts))
        for contact_list in contact_lists[1:]:
            if not contact_list.contacts or not contacts:
                return []
            contacts &= set(map(lambda c: c.to_object, contact_list.contacts))
        return list(contacts)
    else:
        raise ValueError()


def _check_edit_permissions(contact_list):
    mtool = ploneapi.portal.get_tool('portal_membership')
    if not (mtool.checkPermission('cmf.ModifyPortalContent', contact_list) or
                mtool.checkPermission('Modify portal content', contact_list)):
        raise Unauthorized("You can't edit this contact list")

from copy import deepcopy
from collective.contact.widget.source import ContactSourceBinder, ContactSource
from collective.contact.contactlist import api
from plone import api as ploneapi


class ContactListSource(ContactSource):
    contact_lists_query = None

    def __init__(self, context, contact_lists_query=None, contact_lists_operator=None, **kwargs):
        self.contact_lists_query = contact_lists_query
        self.contact_lists_operator = contact_lists_operator
        ContactSource.__init__(self, context, **kwargs)

    def search(self, query, **kwargs):
        # get contact lists
        contact_lists = [cl.getObject()
                         for cl in ploneapi.content.find(**self.contact_lists_query)]
        if len(contact_lists) == 0:
            return []

        # get contacts from lists
        contact_lists_contacts = api.get_contacts(
            *contact_lists, operator=self.contact_lists_operator)
        if len(contact_lists_contacts) == 0:
            return []

        lists_contacts_tokens = [
            "/".join(contact.getPhysicalPath())
            for contact in contact_lists_contacts
            ]

        # get query_results
        if len(self.selectable_filter.criteria) == len(query) == 0:
            return (self.getTermByToken(token) for token in lists_contacts_tokens)

        contacts_query_result = list(super(ContactListSource, self).search(query, **kwargs))
        return (query_contact for query_contact in contacts_query_result
                if query_contact.token in lists_contacts_tokens)


class ContactListSourceBinder(ContactSourceBinder):
    path_source = ContactListSource

    def __init__(self, contact_lists_query, contact_lists_operator='or', **kwargs):
        ContactSourceBinder.__init__(self, **kwargs)

        contact_lists_query = deepcopy(contact_lists_query)
        if 'portal_type' not in contact_lists_query:
            contact_lists_query['portal_type'] = 'contact_list'

        self.contact_lists_query = contact_lists_query
        self.contact_lists_operator = contact_lists_operator

    def __call__(self, context):
        source = super(ContactSourceBinder, self).__call__(context)
        source.contact_lists_query = self.contact_lists_query
        source.contact_lists_operator = self.contact_lists_operator
        return source

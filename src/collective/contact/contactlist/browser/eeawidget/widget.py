""" Select widget
"""
from zope.interface import Interface
from zope.interface import implements
from plone import api

from eea.facetednavigation.widgets.checkbox.widget import Widget as CheckboxWidget
from eea.facetednavigation import EEAMessageFactory as _

from collective.contact.contactlist.api import get_contacts
from plone.uuid.interfaces import IUUID


# Archetypes
EditSchema = CheckboxWidget.edit_schema.copy()
EditSchema['vocabulary'].default = 'collective.contact.contactlist.lists'
EditSchema['vocabulary'].vocabulary_factory='collective.contact.contactlist.vocabularies'
EditSchema['index'].default = 'UID'
EditSchema['index'].widget.visible = -1


class IContactListWidget(Interface):
    pass


class Widget(CheckboxWidget):
    """ Widget
    """
    implements(IContactListWidget)
    # Widget properties
    widget_type = 'contactlist'
    widget_label = _('Contact lists')
    css_class = 'faceted-checkboxes-widget faceted-contactlist-widget'

    edit_schema = EditSchema

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '') or 'UID'
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        if not value:
            return query

        contact_lists = api.portal.get_tool('portal_catalog')(UID=value)
        contacts = get_contacts(*[c.getObject() for c in contact_lists],
                                operator=self.data.get('operator', 'or'))
        contact_uids = [IUUID(c) for c in contacts]
        query[index] = contact_uids
        return query

    def count(self, brains, sequence=None):
        """ Intersect results
        """
        res = {}
        if not sequence:
            sequence = [key for key, value in self.vocabulary()]

        if not sequence:
            return res

        index_id = self.data.get('index')
        if not index_id:
            return res

        brain_uids = {b.UID for b in brains}
        res[""] = res['all'] = len(brain_uids)
        for list_uid in sequence:
            contacts = get_contacts(api.content.get(UID=list_uid))
            list_contact_uids = {c.UID() for c in contacts}
            num = len(brain_uids.intersection(list_contact_uids))
            res[list_uid] = num

        return res

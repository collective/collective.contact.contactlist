""" Select widget
"""
from collective.contact.contactlist.api import get_contacts
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets.checkbox.interfaces import ICheckboxSchema
from eea.facetednavigation.widgets.checkbox.widget import Widget as CheckboxWidget
from plone import api
from plone.uuid.interfaces import IUUID
from zope.interface import implements
from zope.interface import Interface

import copy


class IContactListSchema(ICheckboxSchema):
    pass


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

    def updateWidgets(self, prefix=None):
        super(Widget, self).updateWidgets(prefix=prefix)
        group = [g for g in self.groups if g.label == u'default'][0]
        voc_fld = group.fields['vocabulary']
        voc_fld.field = copy.copy(voc_fld.field)
        voc_fld.field.vocabularyName = u'collective.contact.contactlist.vocabularies'
        ind_fld = group.fields['index']
        ind_fld.field = copy.copy(ind_fld.field)
        ind_fld.field.readonly = True

    def update(self):
        super(Widget, self).update()
        group = [g for g in self.groups if g.label == u'default'][0]
        voc_wd = group.widgets['vocabulary']
        voc_wd.value = ['collective.contact.contactlist.lists']
        ind_wd = group.widgets['index']
        ind_wd.value = ['UID']

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

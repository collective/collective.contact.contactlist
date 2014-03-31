from five import grok
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from grokcore.component.directive import name

from collective.contact.contactlist.api import get_user_lists_adapter
from collective.contact.contactlist import _
from plone import api

class ListsVocabulary(grok.GlobalUtility):
    """All lists user can see
    """
    grok.name('collective.contact.contactlist.lists')
    grok.implements(IVocabularyFactory)

    @classmethod
    def name(self):
        return name.bind().get(self)

    def _sorted_lists(self, lists):
        user_id = api.user.get_current().getId()
        def sort_lists(list1, list2):
            if list1.Creator() == list2.Creator():
                return cmp(list1.Title(), list2.Title())
            elif list1.Creator() == user_id:
                return -1
            elif list2.Creator() == user_id:
                return 1

            return sorted(lists, cmp=sort_lists)

        return sorted(lists, cmp=sort_lists)

    def _get_terms(self, contact_lists):
        return [SimpleVocabulary.createTerm(
                     b.UID(),
                     b.UID(),
                     self.render_list(b))
                 for b in contact_lists]

    def render_list(self, contact_list):
        creator = contact_list.Creator()
        if creator == api.user.get_current().getId():
            return contact_list.Title()
        else:
            user = api.user.get(creator)
            fullname = user and user.getProperty('fullname', '') or creator
            return "%s (%s)" % (contact_list.Title(),
                                fullname)

    def _get_lists(self):
        lists = get_user_lists_adapter().get_lists()
        lists = self._sorted_lists(lists)
        return lists

    def __call__(self, context):
        lists = self._get_lists()
        return SimpleVocabulary(self._get_terms(lists))


class EditableListsVocabulary(ListsVocabulary):
    """All lists user can edit
    """
    grok.name('collective.contact.contactlist.editablelists')

    def _get_lists(self):
        editable_lists = get_user_lists_adapter().get_editable_lists()
        editable_lists = self._sorted_lists(editable_lists)
        return editable_lists


class MyListsVocabulary(ListsVocabulary):
    """All lists created by user
    """
    grok.name('collective.contact.contactlist.mylists')

    def _get_lists(self):
        return get_user_lists_adapter().get_my_lists()


CREATE_NEW_KEY = 'create-new-list'

class AddToListVocabulary(EditableListsVocabulary):
    """All lists user can edit + list creation option
    """
    grok.name('collective.contact.contactlist.addtolist')

    def __call__(self, context):
        lists = self._get_lists()
        terms = self._get_terms(lists)
        terms.append(SimpleVocabulary.createTerm(CREATE_NEW_KEY,
                                                 CREATE_NEW_KEY,
                                                 _(u"Create a new list")))
        return SimpleVocabulary(terms)


class ContactListVocabularies(grok.GlobalUtility):
    grok.name('collective.contact.contactlist.vocabularies')
    grok.implements(IVocabularyFactory)
    vocabularies = (ListsVocabulary, MyListsVocabulary, EditableListsVocabulary)

    def __call__(self, context):
        return SimpleVocabulary(
                [SimpleVocabulary.createTerm(
                     b.name(),
                     b.name(),
                     b.__doc__)
                 for b in self.vocabularies])
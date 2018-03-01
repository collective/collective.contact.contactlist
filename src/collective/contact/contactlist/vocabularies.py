from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from plone import api

from collective.contact.contactlist.api import get_tool
from collective.contact.contactlist import _


class ListsVocabulary(object):
    """All lists user can see.
    Lists shared to user are distinguished with owner's name.
    """
    implements(IVocabularyFactory)
    name = 'collective.contact.contactlist.lists'

    def _sorted_lists(self, lists):
        user_id = api.user.get_current().getId()

        def sort_lists(list1, list2):
            list1_creator, list2_creator = list1.Creator(), list2.Creator()
            if list1_creator == user_id and list1_creator != list2_creator:
                return -1
            elif list2_creator == user_id and list1_creator != list2_creator:
                return 1
            else:
                return cmp(list1.Title().lower(), list2.Title().lower())

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
        lists = get_tool().get_lists()
        lists = self._sorted_lists(lists)
        return lists

    def __call__(self, context):
        lists = self._get_lists()
        return SimpleVocabulary(self._get_terms(lists))


def _list_sort_key(x):
    return x.Title().lower()


class EditableListsVocabulary(ListsVocabulary):
    """All lists user can edit, sorted by creator
    """
    name = 'collective.contact.contactlist.editablelists'

    def _get_lists(self):
        editable_lists = get_tool().get_editable_lists()
        editable_lists = self._sorted_lists(editable_lists)
        return editable_lists


class AllListsVocabulary(ListsVocabulary):
    """All lists user can view, without distinction
    """
    name = 'collective.contact.contactlist.alllists'

    def _sorted_lists(self, lists):
        return sorted(lists, key=_list_sort_key)

    def render_list(self, contact_list):
        return contact_list.Title()


class MyListsVocabulary(AllListsVocabulary):
    """All lists created by user
    """
    name = 'collective.contact.contactlist.mylists'

    def _get_lists(self):
        return self._sorted_lists(get_tool().get_my_lists())


CREATE_NEW_KEY = 'create-new-list'


class AddToListVocabulary(EditableListsVocabulary):
    """All lists user can edit + list creation option
    """
    name = 'collective.contact.contactlist.addtolist'

    def __call__(self, context):
        terms = [SimpleVocabulary.createTerm(CREATE_NEW_KEY,
                                             CREATE_NEW_KEY,
                                             _(u"Create a new list"))]
        lists = self._get_lists()
        terms.extend(self._get_terms(lists))
        return SimpleVocabulary(terms)


class ContactListVocabularies(object):
    """Vocabulary of vocabularies, for eea.facetednavigation for instance
    """
    name = 'collective.contact.contactlist.vocabularies'
    implements(IVocabularyFactory)
    vocabularies = (ListsVocabulary, MyListsVocabulary, EditableListsVocabulary,
                    AllListsVocabulary)

    def __call__(self, context):
        return SimpleVocabulary(
                [SimpleVocabulary.createTerm(
                     b.name,
                     b.name,
                     b.__doc__)
                 for b in self.vocabularies])

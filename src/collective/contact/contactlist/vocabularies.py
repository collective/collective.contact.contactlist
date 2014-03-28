from five import grok
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from grokcore.component.directive import name

from plone.uuid.interfaces import IUUID

from collective.contact.contactlist.api import get_user_lists_adapter
from collective.contact.contactlist import _

class ListsVocabulary(grok.GlobalUtility):
    """All lists user can see
    """
    grok.name('collective.contact.contactlist.lists')
    grok.implements(IVocabularyFactory)

    @classmethod
    def name(self):
        return name.bind().get(self)

    def _get_terms(self):
        return [SimpleVocabulary.createTerm(
                     b.UID,
                     b.UID,
                     b.Title)
                 for b in get_user_lists_adapter().get_lists_brains()]


    def __call__(self, context):
        terms = self._get_terms()
        return SimpleVocabulary(terms)


class EditableListsVocabulary(ListsVocabulary):
    """All lists user can edit
    """
    grok.name('collective.contact.contactlist.editablelists')

    def _get_terms(self):
        return [SimpleVocabulary.createTerm(
                     IUUID(b),
                     IUUID(b),
                     b.Title())
                 for b in get_user_lists_adapter().get_editable_lists()]


class MyListsVocabulary(ListsVocabulary):
    """All lists created by user
    """
    grok.name('collective.contact.contactlist.mylists')

    def _get_terms(self):
        return [SimpleVocabulary.createTerm(
                     IUUID(b),
                     IUUID(b),
                     b.Title())
                 for b in get_user_lists_adapter().get_my_lists()]


CREATE_NEW_KEY = 'create-new-list'

class AddToListVocabulary(EditableListsVocabulary):
    """All lists user can edit + list creation option
    """
    grok.name('collective.contact.contactlist.addtolist')

    def __call__(self, context):
        terms = self._get_terms()
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
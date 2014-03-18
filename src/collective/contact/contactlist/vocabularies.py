from five import grok
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from plone.uuid.interfaces import IUUID

from collective.contact.contactlist.api import get_user_lists_adapter
from collective.contact.contactlist import _

class ListsVocabulary(grok.GlobalUtility):
    grok.name('collective.contact.contactlist.lists')
    grok.implements(IVocabularyFactory)

    def _get_terms(self):
        return [SimpleVocabulary.createTerm(
                     b.UID,
                     b.UID,
                     b.Title)
                 for b in get_user_lists_adapter().get_list_brains()]


    def __call__(self, context):
        terms = self._get_terms()
        return SimpleVocabulary(terms)


class EditableListsVocabulary(ListsVocabulary):
    grok.name('collective.contact.contactlist.editablelists')

    def _get_terms(self):
        return [SimpleVocabulary.createTerm(
                     IUUID(b),
                     IUUID(b),
                     b.Title())
                 for b in get_user_lists_adapter().get_editable_lists()]

CREATE_NEW_KEY = 'create-new-list'

class AddToListVocabulary(EditableListsVocabulary):
    grok.name('collective.contact.contactlist.addtolist')

    def __call__(self, context):
        terms = self._get_terms()
        terms.append(SimpleVocabulary.createTerm(CREATE_NEW_KEY,
                                                 CREATE_NEW_KEY,
                                                 _(u"Create a new list")))
        return SimpleVocabulary(terms)

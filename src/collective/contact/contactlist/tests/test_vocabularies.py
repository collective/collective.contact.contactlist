from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.testing import expectedFailureOnPlone4
from collective.contact.contactlist.testing import IntegrationTestCase
from collective.contact.contactlist.vocabularies import CREATE_NEW_KEY
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TestVocabularies(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        army = self.portal.mydirectory.armeedeterre
        login(self.portal, TEST_USER_NAME)
        create_list("Corpses", "Description of my list", [army.corpsa, army.corpsb])
        login(self.portal, "testuser")
        create_list(
            "Divisions",
            "Description of my list",
            [army.corpsa.divisionalpha, army.corpsb],
        )
        create_list("armies", "", [army])

    def titles(self, name):
        return [t.title for t in getUtility(IVocabularyFactory, name=name)(self.portal)]

    def test_ListsVocabulary(self):
        # current user's lists first, other lists with their creator's fullname
        self.assertEqual(
            self.titles("collective.contact.contactlist.lists"),
            ["armies", "Divisions", "Corpses (%s)" % TEST_USER_ID],
        )
        login(self.portal, TEST_USER_NAME)
        self.assertEqual(
            self.titles("collective.contact.contactlist.lists"),
            ["Corpses", "armies (Test user)", "Divisions (Test user)"],
        )

    def test_EditableListsVocabulary(self):
        self.assertEqual(
            self.titles("collective.contact.contactlist.editablelists"),
            ["armies", "Divisions", "Corpses (%s)" % TEST_USER_ID],
        )
        # a plain member can't edit lists of other users
        login(self.portal, "member")
        self.assertEqual(
            self.titles("collective.contact.contactlist.editablelists"), []
        )

    def test_AllListsVocabulary(self):
        self.assertEqual(
            self.titles("collective.contact.contactlist.alllists"),
            ["armies", "Corpses", "Divisions"],
        )

    def test_MyListsVocabulary(self):
        self.assertEqual(
            self.titles("collective.contact.contactlist.mylists"),
            ["armies", "Divisions"],
        )

    @expectedFailureOnPlone4  # AttributeError: 'NoneType' object has no attribute 'values'
    def test_MyListsVocabulary_without_user_folder(self):
        login(self.portal, "member")
        self.assertEqual(self.titles("collective.contact.contactlist.mylists"), [])

    def test_AddToListVocabulary(self):
        vocabulary = getUtility(
            IVocabularyFactory, name="collective.contact.contactlist.addtolist"
        )(self.portal)
        self.assertEqual([t.token for t in vocabulary][0], CREATE_NEW_KEY)
        self.assertEqual(
            [t.title for t in vocabulary][1:],
            ["armies", "Divisions", "Corpses (%s)" % TEST_USER_ID],
        )
        # a plain member can only create a list
        login(self.portal, "member")
        vocabulary = getUtility(
            IVocabularyFactory, name="collective.contact.contactlist.addtolist"
        )(self.portal)
        self.assertEqual([t.token for t in vocabulary], [CREATE_NEW_KEY])

    def test_ContactListVocabularies(self):
        vocabulary = getUtility(
            IVocabularyFactory, name="collective.contact.contactlist.vocabularies"
        )(self.portal)
        self.assertEqual(
            [t.token for t in vocabulary],
            [
                "collective.contact.contactlist.lists",
                "collective.contact.contactlist.mylists",
                "collective.contact.contactlist.editablelists",
                "collective.contact.contactlist.alllists",
            ],
        )

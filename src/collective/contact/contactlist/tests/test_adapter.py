from collective.contact.contactlist.api import create_list
from collective.contact.contactlist.api import get_tool
from collective.contact.contactlist.testing import expectedFailureOnPlone4
from collective.contact.contactlist.testing import IntegrationTestCase
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME


class TestUserListStorage(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        army = self.portal.mydirectory.armeedeterre
        login(self.portal, TEST_USER_NAME)
        self.list_1 = create_list(
            "Corpses", "Description of my list", [army.corpsa, army.corpsb]
        )
        login(self.portal, "testuser")
        self.list_2 = create_list(
            "Divisions",
            "Description of my list",
            [army.corpsa.divisionalpha, army.corpsb],
        )

    def test_get_lists_brains(self):
        self.assertEqual(
            sorted([b.getPath() for b in get_tool().get_lists_brains()]),
            [
                "/plone/Members/%s/corpses" % TEST_USER_ID,
                "/plone/Members/testuser/divisions",
            ],
        )

    def test_get_lists(self):
        # the sort order is undefined
        self.assertListsHaveSameContents(
            get_tool().get_lists(), [self.list_1, self.list_2]
        )
        login(self.portal, "member")
        self.assertListsHaveSameContents(
            get_tool().get_lists(), [self.list_1, self.list_2]
        )

    def test_get_editable_lists(self):
        self.assertListsHaveSameContents(
            get_tool().get_editable_lists(), [self.list_1, self.list_2]
        )
        # a plain member can't edit lists of other users
        login(self.portal, "member")
        self.assertEqual(get_tool().get_editable_lists(), [])

    def test_get_my_lists(self):
        self.assertEqual(get_tool().get_my_lists(), [self.list_2])

    @expectedFailureOnPlone4  # AttributeError: 'NoneType' object has no attribute 'values'
    def test_get_my_lists_without_user_folder(self):
        # a user without user folder has no lists
        login(self.portal, "member")
        self.assertEqual(get_tool().get_my_lists(), [])

    def test_get_container(self):
        self.assertEqual(get_tool().get_container(), self.portal.Members["testuser"])
        login(self.portal, TEST_USER_NAME)
        self.assertEqual(get_tool().get_container(), self.portal.Members[TEST_USER_ID])
        # a user without user folder
        login(self.portal, "member")
        self.assertIsNone(get_tool().get_container())
        # anonymous
        logout()
        self.assertIsNone(get_tool().get_container())

    @expectedFailureOnPlone4  # AttributeError: Members
    def test_get_container_without_members_folder(self):
        # a site without Members folder, as created without the example content
        login(self.portal, "testuser")
        api.content.delete(self.portal.Members, check_linkintegrity=False)
        self.assertIsNone(get_tool().get_container())

    def test_get_lists_for_contact(self):
        army = self.portal.mydirectory.armeedeterre
        self.assertListsHaveSameContents(
            get_tool().get_lists_for_contact(army.corpsb), [self.list_1, self.list_2]
        )
        self.assertListsHaveSameContents(
            get_tool().get_lists_for_contact(army.corpsa), [self.list_1]
        )
        self.assertEqual(get_tool().get_lists_for_contact(army), [])

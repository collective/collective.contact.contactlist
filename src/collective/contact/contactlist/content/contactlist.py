from collective.contact.contactlist.interfaces import IContactList
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from zope.interface import implementer


@implementer(IContactList)
class ContactList(Container):
    """ContactList content type"""


class ContactListSchemaPolicy(DexteritySchemaPolicy):
    """Schema policy for ContactList content type"""

    def bases(self, schemaName, tree):
        return (IContactList, )

from zope.interface import implements

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.contact.contactlist.interfaces import IContactList


class ContactList(Container):
    """ContactList content type"""
    implements(IContactList)


class ContactListSchemaPolicy(DexteritySchemaPolicy):
    """Schema policy for ContactList content type"""

    def bases(self, schemaName, tree):
        return (IContactList, )

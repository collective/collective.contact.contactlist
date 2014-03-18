from zope.interface import implements

from five import grok

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.contact.contactlist.interfaces import IContactList


class ContactList(Container):
    """ContactList content type"""
    implements(IContactList)


class ContactListSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    """Schema policy for ContactList content type"""
    grok.name("schema_policy_contact_list")

    def bases(self, schemaName, tree):
        return (IContactList, )

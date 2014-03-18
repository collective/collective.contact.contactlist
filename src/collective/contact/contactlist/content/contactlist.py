from zope.interface import implements

from five import grok

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.supermodel import model

from collective.contact.widget import schema
from collective.contact.contactlist import _


class IContactList(model.Schema):
    """Interface for ContactList content type"""

    contacts = schema.ContactList(
        title=_("Contacts of the list"),
        )

class ContactList(Container):
    """ContactList content type"""
    implements(IContactList)


class ContactListSchemaPolicy(grok.GlobalUtility, DexteritySchemaPolicy):
    """Schema policy for ContactList content type"""
    grok.name("schema_policy_contact_list")

    def bases(self, schemaName, tree):
        return (IContactList, )

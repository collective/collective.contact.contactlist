==========================================================================
collective.contact.contactlist
==========================================================================

This add-on is part of the ``collective.contact.*`` suite. For an overview and a demo of these suite, see `collective.contact.demo <https://github.com/collective/collective.contact.demo>`__.

Users can can manage lists of contacts.
Adds an action to search and add a content to an existing or a new list.

Lists handles any contact type: organization, person or held position.


Installation
============

You need to turn on Member folder creation.

API
===

An helper api to manage contact lists: ::

    def extend_list(contact_list, contacts):
        """Add contacts to a contact list
        @param contact_list: object - The contact list object
        @param contacts: objects - A list of contact objects
        @return: objects - the list of contacts that have been actually added
        """

    def replace_list(contact_list, contacts):
        """Replace the contacts of a contact list
        @param contact_list: object - The contact list object
        @param contacts: objects - A list of contact objects
        @return: objects - the list of contacts that have been actually added
        """

    def get_contacts(*contact_lists, **kwargs):
        """Get the contacts from one or many contact list(s)
        kwargs can have an 'operator' option ('and' or 'or')
        so we make union or intersection of lists
        default is 'or'
        """


Vocabularies
============

- `collective.contact.contactlist.lists`: all lists user can see.
  Lists shared to user are distinguished with owner's name.
- `collective.contact.contactlist.alllists`: all lists user can view, without distinction,
- `collective.contact.contactlist.editablelists`: all lists user can edit,
- `collective.contact.contactlist.mylists`: all lists created by user,
- `collective.contact.contactlist.addtolist`: all lists user can edit + list creation option
- `collective.contact.contactlist.vocabularies`: vocabulary of all previous vocabularies.


Integration with collective.contact.facetednav
==============================================

If you have collective.contact.facetednav installed,
if you have enabled contact selection on your faceted navigation
you can batch select contacts and add them to lists

You have a new widget "contacts list", wich display your lists.
It filters your results on the contents of the lists you have selected.

Compatible with eea.facetednav < 10

Use ContactListSourceBinder
===========================

When you write a schema,
you can filter choices of a ContactChoice (or ContactList) field on the contacts of one or many lists: ::

        birthday_guests = ContactList(
            title=u"Birthday guests",
            value_type=ContactChoice(
                source=ContactListSourceBinder(
                    contact_lists_query={'Subject': 'Friends'}),
                    contact_lists_operator='or',
                    portal_type=("person",),
                )
            )
        )

This works like ContactSourceBinder from collective.contact.widget, but it also gets a
countact_lists_query parameter, wich is a catalog query dictionnary. Contacts displayed by formwidget
query are filtered on the union or intersection (depending on contact_lists_operator) of the lists we get using this query.


Tests
=====

This add-on is tested using Travis CI. The current status of the add-on is :

.. image:: https://secure.travis-ci.org/collective/collective.contact.contactlist.png
    :target: http://travis-ci.org/collective/collective.contact.contactlist

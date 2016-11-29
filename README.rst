==========================================================================
collective.contact.contactlist
==========================================================================

This add-on is part of the ``collective.contact.*`` suite. For an overview and a demo of these suite, see `collective.contact.demo <https://github.com/collective/collective.contact.demo>`__.

Users can can manage lists of contacts.
Adds an action to add a content to an existing or a new list.

Installation
============

By default, you need to turn on Member folder creation.

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

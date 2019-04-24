Changelog
=========


2.0 (2019-04-24)
----------------

- Made it compatible with eea.facetednavigation >= 10.0. Branch 1.x is compatible with eea.facetednavigation < 10.0
  [sgeulette]

1.3 (2018-11-13)
----------------

- 'collective.contact.contactlist.lists' vocabulary is sorted by title when creators are different.
  + few fixes on list order
  [thomasdesvenain]


1.2 (2017-01-17)
----------------

- Test eea widget.
  [thomasdesvenain]

- API: Added a source binder that allows developers
  to restrict ContactChoice fields on contents of contact lists.
  [thomasdesvenain]

- get_contacts with 'and' operator was broken.
  [thomasdesvenain]

- Minor optimizations and PEP8.
  [thomasdesvenain]

- API: deprecate update_list function and create extend_list instead,
  which is less ambiguous.
  [thomasdesvenain]

- Fix get_contacts API for empty list
  [ebrehault]


1.1 (2016-09-23)
----------------

- More robust unit tests.
  [thomasdesvenain]

- Add get_lists_for_contact method to get all lists that contain contact.
  [cedricmessiant]

- Fix relations.
  [cedricmessiant]

- Put 'Create a new list' on top of the select widget.
  [cedricmessiant]

- Fix update_list API for empty list
  [ebrehault]

- Fix permissions in API
  [ebrehault]


1.0 (2014-06-16)
----------------

- Initial release.
  [tdesvenain]

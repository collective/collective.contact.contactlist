Changelog
=========


3.0.0 (unreleased)
------------------

- Migrate to Plone 6.2, drop Plone 4 support, based on the work started on `plone6` with @laulaz.
  [laulaz, chris-adam]
- Faceted batch actions: open the modal with `patPloneModal` (it never opened), escape the added contacts, CSRF token on the forms.
  [chris-adam]
- Plone 6 migration:
  replaced the Plone 4 overlays with `pat-plone-modal` (the "Add to list" action uses the
  action `modal` property, faceted navigation batch actions open the modal in JavaScript),
  used `plone.base.interfaces.IBundleRegistry` and a `contenttype/contact_list` icon,
  enabled user folders with the `plone.enable_user_folders` record and created the `Members` folder
  on install (Plone 6 only adds it with the example content),
  added an uninstall profile and fixed Python 3 / Plone 6 incompatibilities
  (sorting with `cmp`, `from_interfaces_flattened` relation query, tests).
  [chris-adam]
- Allowed the "Add to list" form to be prefilled by the GET request of the action
  (`allow_prefill_from_GET_request`): the selected contact was ignored.
  [chris-adam]
- Registered the user lists adapter for (user, portal, request) only: as an adapter of
  (Interface, Interface, Interface), it was used as add view by `++add++contact_list`.
  [chris-adam]
- Used the excel mimetype icon of the icon resolver in the excel export link (`xls.png` is gone).
  [chris-adam]
- Restructured the unit tests (one test module per module), added robot tests
  (`make robot`, `make robot-server`).
  [chris-adam]


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

*** Settings ***
Documentation  Integration with the contacts faceted navigation (collective.contact.facetednav):
...            "Add to list" and "Replace list" batch actions and the "Contact lists" filter.
...            In Plone 4, the batch actions opened an overlay that, after saving, showed the
...            status message in the batch actions, refreshed the results and the list counts
...            without reloading the page.
Resource  contactlist.robot
Test Setup  Run keywords  Open test browser  AND  Log in as manager testuser
Test Teardown  Close all browsers


*** Variables ***
${BATCH_ACTIONS}  css=#contacts-facetednav-batchactions
${ADD_TO_LIST}  css=#contact-facetednav-action-addtolist
${REPLACE_LIST}  css=#contact-facetednav-action-replace
${LISTS_WIDGET}  css=#lists_widget


*** Keywords ***
Go to the faceted directory
    Go to  ${DIRECTORY_URL}
    Wait until element is visible  css=.eea-preview-items
    The faceted query is done

The faceted query is done
    [Documentation]  the page shows the results rendered by the server until the first query (Plone 6),
    ...              eea.facetednavigation locks the page during the queries and the counts
    Wait until element is not visible  css=.faceted-lock-overlay

Select the contact
    [Arguments]  ${path}
    ${uid}=  Path to uid  ${path}
    # once the contacts of the results are loaded (json-contacts)
    Wait for condition  return contactfacetednav.contacts.get('${uid}') !== undefined
    Select checkbox  css=#contact-${uid}

Check the list in the "Contact lists" filter
    [Arguments]  ${path}
    ${uid}=  Path to uid  ${path}
    Select checkbox  ${LISTS_WIDGET} input[value="${uid}"]
    Wait until element is visible  css=.eea-preview-items
    The faceted query is done


*** Test Cases ***
The batch actions need a selection
    Go to the faceted directory
    Element should be visible  ${ADD_TO_LIST}
    Element should be visible  ${REPLACE_LIST}
    Element should be disabled  ${ADD_TO_LIST}
    Select the contact  /plone/mydirectory/armeedeterre/corpsa
    Element should be enabled  ${ADD_TO_LIST}
    Element should be enabled  ${REPLACE_LIST}

Add the selected contacts to a new list
    Go to the faceted directory
    Select the contact  /plone/mydirectory/armeedeterre/corpsa
    Select the contact  /plone/mydirectory/armeedeterre/corpsb
    Click button  ${ADD_TO_LIST}
    The modal is open
    Wait until element is visible  ${MODAL} #form-widgets-title
    Page should contain element  ${MODAL} input[type=hidden][value="/plone/mydirectory/armeedeterre/corpsa"]
    Page should contain element  ${MODAL} input[type=hidden][value="/plone/mydirectory/armeedeterre/corpsb"]
    Input text  ${MODAL} #form-widgets-title  Faceted list
    Save the modal
    The modal is closed
    # no reload: the message is shown in the batch actions
    # (eea.facetednavigation keeps the query in the URL hash)
    Location should contain  ${DIRECTORY_URL}
    Wait until element contains  ${BATCH_ACTIONS}  New list added with 2 contact(s) : Faceted list
    The list contains  ${PLONE_URL}/Members/testuser/faceted-list  Corps A  Corps B

Replace the list checked in the filter
    Create a list with the contact  testuser  faceted-list  Faceted list  /plone/mydirectory/armeedeterre/corpsa
    Go to the faceted directory
    Check the list in the "Contact lists" filter  /plone/Members/testuser/faceted-list
    Select the contact  /plone/mydirectory/armeedeterre/corpsa
    Click button  ${REPLACE_LIST}
    The modal is open
    Wait until element is visible  ${MODAL} #form-widgets-contact_list
    ${uid}=  Path to uid  /plone/Members/testuser/faceted-list
    List selection should be  ${MODAL} #form-widgets-contact_list  ${uid}
    Save the modal
    The modal is closed
    Wait until element contains  ${BATCH_ACTIONS}  Faceted list list contacts has been replaced by 1 contact(s)

Add the selected contacts to a list of the filter
    [Documentation]  the "Contact lists" filter only shows the lists that existed when the page was loaded:
    ...              their counts are updated
    Create a list with the contact  testuser  faceted-list  Faceted list  /plone/mydirectory/armeedeterre/corpsa
    Go to the faceted directory
    # the counts are loaded after the results
    Wait until element contains  ${LISTS_WIDGET}  Faceted list (1)
    Select the contact  /plone/mydirectory/armeedeterre/corpsb
    Click button  ${ADD_TO_LIST}
    The modal is open
    Wait until element is visible  ${MODAL} #form-widgets-contact_list
    Select from list by label  ${MODAL} #form-widgets-contact_list  Faceted list
    Save the modal
    The modal is closed
    Wait until element contains  ${BATCH_ACTIONS}  Faceted list list updated with 1 contact(s)
    Wait until element contains  ${LISTS_WIDGET}  Faceted list (2)

Filter the contacts by list
    Create a list with the contact  testuser  faceted-list  Faceted list  /plone/mydirectory/armeedeterre/corpsa
    Go to the faceted directory
    Wait until element contains  ${LISTS_WIDGET}  Faceted list (1)
    Check the list in the "Contact lists" filter  /plone/Members/testuser/faceted-list
    Element should contain  css=.eea-preview-items  Corps A
    Element should not contain  css=.eea-preview-items  Corps B

*** Settings ***
Documentation  The contact_list content type: icon, add and edit forms.
Resource  contactlist.robot
Test Setup  Run keywords  Open test browser  AND  Log in as manager testuser
Test Teardown  Close all browsers


*** Variables ***
${CORPSA_TOKEN}  /plone/mydirectory/armeedeterre/corpsa
${CONTACTS_FIELD}  css=#formfield-form-widgets-contacts


*** Keywords ***
Select a contact with the autocomplete
    [Arguments]  ${search}  ${token}
    Input text  css=#form-widgets-contacts-widgets-query  ${search}
    Wait until element is visible  css=li.search-result[data-token="${token}"]
    Click element  css=li.search-result[data-token="${token}"]
    Wait until page contains element  ${CONTACTS_FIELD} input[type=checkbox][value="${token}"]


*** Test Cases ***
The Add menu shows the contact list icon
    Go to  ${PLONE_URL}/Members/testuser
    Click element  css=#plone-contentmenu-factories > a
    Wait until element is visible  css=#plone-contentmenu-factories a#contact_list
    Page should contain element  css=#plone-contentmenu-factories a#contact_list svg.bi-person-lines-fill

Add a list with the contacts autocomplete
    Go to  ${PLONE_URL}/Members/testuser/++add++contact_list
    Input text  css=#form-widgets-IBasic-title  Autocomplete list
    Select a contact with the autocomplete  corps  ${CORPSA_TOKEN}
    Click button  css=#form-buttons-save
    Wait until page contains  Item created
    Location should be  ${PLONE_URL}/Members/testuser/autocomplete-list/view
    Element should contain  css=#content-core  Corps A

Remove a contact while editing a list
    Add the contact to a new list  ${ARMY_URL}/corpsa  Edited list
    Go to  ${PLONE_URL}/Members/testuser/edited-list/edit
    Checkbox should be selected  ${CONTACTS_FIELD} input[value="${CORPSA_TOKEN}"]
    Select a contact with the autocomplete  corps  /plone/mydirectory/armeedeterre/corpsb
    Unselect checkbox  ${CONTACTS_FIELD} input[value="${CORPSA_TOKEN}"]
    Click button  css=#form-buttons-save
    Wait until page contains  Changes saved
    Element should contain  css=#content-core  Corps B
    Element should not contain  css=#content-core  Corps A

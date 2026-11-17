*** Settings ***
Documentation  The contact_list content type: icon, add and edit forms.
Resource  contactlist.robot
Test Setup  Run keywords  Open test browser  AND  Log in as manager testuser
Test Teardown  Close all browsers


*** Variables ***
${CORPSA_TOKEN}  /plone/mydirectory/armeedeterre/corpsa
${CONTACTS_FIELD}  css=#formfield-form-widgets-contacts


*** Test Cases ***
The Add menu shows the contact list icon
    Go to  ${PLONE_URL}/Members/testuser
    Open the add menu
    Wait until element is visible  css=#plone-contentmenu-factories a#contact_list
    The add menu item has the icon  contact_list  ${CONTACT_LIST_ICON}

Add a list with the contacts autocomplete
    Go to  ${PLONE_URL}/Members/testuser/++add++contact_list
    Input text  css=#form-widgets-IBasic-title  Autocomplete list
    Select in the contact autocomplete  contacts  corps  ${CORPSA_TOKEN}  Corps A
    Click button  css=#form-buttons-save
    Wait until page contains  Item created
    Location should be  ${PLONE_URL}/Members/testuser/autocomplete-list/view
    Element should contain  css=#content-core  Corps A

Remove a contact while editing a list
    Create a list with the contact  testuser  edited-list  Edited list  ${CORPSA_TOKEN}
    Go to  ${PLONE_URL}/Members/testuser/edited-list/edit
    Checkbox should be selected  ${CONTACTS_FIELD} input[value="${CORPSA_TOKEN}"]
    Select in the contact autocomplete  contacts  corps  /plone/mydirectory/armeedeterre/corpsb  Corps B
    Unselect checkbox  ${CONTACTS_FIELD} input[value="${CORPSA_TOKEN}"]
    Click button  css=#form-buttons-save
    Wait until page contains  Changes saved
    Element should contain  css=#content-core  Corps B
    Element should not contain  css=#content-core  Corps A

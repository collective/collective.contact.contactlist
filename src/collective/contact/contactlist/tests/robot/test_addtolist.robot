*** Settings ***
Documentation  The "Add to list" action of contacts. In Plone 4, it opened an overlay
...            that reloaded the contact page after saving (noform: 'reload').
Resource  contactlist.robot
Test Setup  Run keywords  Open test browser  AND  Log in as manager testuser
Test Teardown  Close all browsers


*** Test Cases ***
The action opens a modal with the contact
    Open the "Add to list" modal  ${ARMY_URL}
    Element should contain  ${MODAL} .modal-title  Add to list
    # the contact is a hidden field of the form
    Page should contain element
    ...  ${MODAL} #formfield-form-widgets-contacts input[type=hidden][value="/plone/mydirectory/armeedeterre"]
    Element should not be visible  ${MODAL} #form-widgets-contacts-widgets-query

The title and description are only asked for a new list
    Create an empty list  testuser  existing  Existing list
    Open the "Add to list" modal  ${ARMY_URL}
    Element should be visible  ${MODAL} #form-widgets-title
    Element should be visible  ${MODAL} #form-widgets-description
    Select from list by label  ${MODAL} #form-widgets-contact_list  Existing list
    Wait until element is not visible  ${MODAL} #form-widgets-title
    Element should not be visible  ${MODAL} #form-widgets-description
    Select from list by label  ${MODAL} #form-widgets-contact_list  Create a new list
    Wait until element is visible  ${MODAL} #form-widgets-title

A new list needs a title
    Open the "Add to list" modal  ${ARMY_URL}
    Save the modal
    Wait until element contains  ${MODAL} #formfield-form-widgets-title  Title of the new list is required

Add a contact to a new list
    Open the "Add to list" modal  ${ARMY_URL}
    Input text  ${MODAL} #form-widgets-title  My new list
    Input text  ${MODAL} #form-widgets-description  Created from a contact
    Save the modal
    The modal is closed
    # the contact page is reloaded
    Location should be  ${ARMY_URL}
    The list contains  ${PLONE_URL}/Members/testuser/my-new-list  My new list  Created from a contact  Armée de terre

Add a contact to an existing list
    Create an empty list  testuser  existing  Existing list
    Open the "Add to list" modal  ${ARMY_URL}/corpsa
    Select from list by label  ${MODAL} #form-widgets-contact_list  Existing list
    Save the modal
    The modal is closed
    Location should be  ${ARMY_URL}/corpsa
    The list contains  ${PLONE_URL}/Members/testuser/existing  Corps A

Add the same contact twice
    Add the contact to a new list  ${ARMY_URL}  My new list
    Open the "Add to list" modal  ${ARMY_URL}
    Select from list by label  ${MODAL} #form-widgets-contact_list  My new list
    Save the modal
    The modal is closed
    Go to  ${PLONE_URL}/Members/testuser/my-new-list
    ${count}=  Get element count  xpath=//*[@id="content-core"]//a[contains(., "Armée de terre")]
    Should be equal as integers  ${count}  1

Cancel closes the modal
    Open the "Add to list" modal  ${ARMY_URL}
    Input text  ${MODAL} #form-widgets-title  Cancelled list
    Click button  css=.modal-footer #form-buttons-cancel
    The modal is closed
    Location should be  ${ARMY_URL}
    Go to  ${PLONE_URL}/Members/testuser/cancelled-list
    Page should contain  This page does not seem to exist

The action is only on contacts
    Go to  ${PLONE_URL}/folder
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions-delete
    Page should not contain element  css=#plone-contentmenu-actions-contactlist-addtolist

*** Settings ***
Documentation  Lists are stored in the user folders: the "My contact lists" personal action
...            and the lists of a plain member.
Resource  contactlist.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
"My contact lists" opens the user folder
    Log in as manager testuser
    Go to  ${PLONE_URL}
    Element attribute value should be  css=#personaltools-contact-contactlist-mylists  href
    ...  ${PLONE_URL}/Members/testuser

A user without user folder has no "My contact lists"
    Enable autologin as  Member
    Set autologin username  member
    Go to  ${PLONE_URL}
    Page should contain element  css=#personaltools-menulink
    Page should not contain element  css=#personaltools-contact-contactlist-mylists

The user folder is created at the first login
    Log in with the login form  member  member123
    Element attribute value should be  css=#personaltools-contact-contactlist-mylists  href
    ...  ${PLONE_URL}/Members/member

A member can only create a new list
    Log in as manager testuser
    Create an empty list  testuser  existing  Existing list
    Log in with the login form  member  member123
    # as in Plone 4, a member doesn't get the Actions menu of contacts
    Go to  ${PLONE_URL}/@@contactlist.add-to-list?form.widgets.contacts:list=/plone/mydirectory/armeedeterre
    ${labels}=  Get list items  css=#form-widgets-contact_list
    Should be equal  ${labels}  ${{ ['Create a new list'] }}
    Input text  css=#form-widgets-title  Member list
    Click button  css=#form-buttons-save
    The list contains  ${PLONE_URL}/Members/member/member-list  Member list  Armée de terre

A member can see the lists of other users but not edit them
    Log in as manager testuser
    Add the contact to a new list  ${ARMY_URL}  Shared list
    Log in with the login form  member  member123
    The list contains  ${PLONE_URL}/Members/testuser/shared-list  Shared list  Armée de terre
    Page should not contain element  css=#contentview-edit

*** Settings ***
Documentation  Package keywords, built on the Plone UI keywords of ui_plone${PLONE_MAJOR}.robot
...            (PLONE_MAJOR is set by test_robot.py).
Resource  ui_plone${PLONE_MAJOR}.robot


*** Variables ***
${DIRECTORY_URL}  ${PLONE_URL}/mydirectory
${ARMY_URL}  ${DIRECTORY_URL}/armeedeterre


*** Keywords ***
Log in as manager testuser
    [Documentation]  testuser is a Manager with a user folder
    Enable autologin as  Manager
    Set autologin username  testuser

Create an empty list
    [Arguments]  ${user}  ${id}  ${title}
    Create content  type=contact_list  container=/plone/Members/${user}  id=${id}  title=${title}

Create a list with the contact
    [Documentation]  without the "Add to list" action, for the scenarios of other features
    [Arguments]  ${user}  ${id}  ${title}  ${contact_path}
    ${uid}=  Create content  type=contact_list  container=/plone/Members/${user}  id=${id}  title=${title}
    ${contact_uid}=  Path to uid  ${contact_path}
    Set field value  ${uid}  contacts  ['${contact_uid}']  references

Open the "Add to list" modal
    [Arguments]  ${contact_url}
    Go to  ${contact_url}
    Click the content action  contactlist-addtolist
    The modal is open
    Wait until element is visible  ${MODAL} #form-widgets-contact_list

Add the contact to a new list
    [Arguments]  ${contact_url}  ${title}
    Open the "Add to list" modal  ${contact_url}
    Input text  ${MODAL} #form-widgets-title  ${title}
    Save the modal
    The modal is closed

The list contains
    [Arguments]  ${list_url}  @{titles}
    Go to  ${list_url}
    FOR  ${title}  IN  @{titles}
        Page should contain  ${title}
    END

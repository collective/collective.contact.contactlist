*** Settings ***
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${DIRECTORY_URL}  ${PLONE_URL}/mydirectory
${ARMY_URL}  ${DIRECTORY_URL}/armeedeterre
${MODAL}  css=.modal-dialog


*** Keywords ***
Log in as manager testuser
    [Documentation]  testuser is a Manager with a user folder
    Enable autologin as  Manager
    Set autologin username  testuser

Log in with the login form
    [Documentation]  a real login creates the user folder
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    Click button  css=#buttons-login
    Wait until page contains element  css=#personaltools-menulink

Create an empty list
    [Arguments]  ${user}  ${id}  ${title}
    Create content  type=contact_list  container=/plone/Members/${user}  id=${id}  title=${title}

Open the "Add to list" modal
    [Arguments]  ${contact_url}
    Go to  ${contact_url}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions-contactlist-addtolist
    Click element  css=#plone-contentmenu-actions-contactlist-addtolist
    Wait until element is visible  ${MODAL} #form-widgets-contact_list

Save the modal
    Click button  css=.modal-footer #form-buttons-save

The modal is closed
    Wait until page does not contain element  ${MODAL}

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

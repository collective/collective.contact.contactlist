*** Settings ***
Documentation  Plone 6 Classic UI keywords. Same keyword names and arguments as ui_plone4.robot.
...            Robot Framework 3.x syntax: shared with the Plone 4.3 (Python 2) environment.
...            Selectors from the scenarios checked on Plone 6.1; not run on Plone 6.2 yet.
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${MODAL}  css=.modal-dialog
${ERROR_PAGE_TEXT}  there seems to be an error
${NOT_FOUND_TEXT}  This page does not seem to exist
${ADDONS_URL}  ${PLONE_URL}/prefs_install_products_form
# icon of the contact_list type: bootstrap icon
${CONTACT_LIST_ICON}  person-lines-fill


*** Keywords ***
Log in with the login form
    [Documentation]  Real login (creates the user folder), unlike autologin
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    Click button  css=#buttons-login
    Wait until page contains element  css=#personaltools-menulink

The user is logged in
    Page should contain element  css=#personaltools-menulink

Click the content action
    [Documentation]  Item of the Actions menu (object_buttons), by action id
    [Arguments]  ${action_id}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions-${action_id}
    Click element  css=#plone-contentmenu-actions-${action_id}

The content action is available
    [Arguments]  ${action_id}  ${expected}=${True}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions ul
    Run keyword if  ${expected}
    ...  Page should contain element  css=#plone-contentmenu-actions-${action_id}
    ...  ELSE  Page should not contain element  css=#plone-contentmenu-actions-${action_id}

Open the add menu
    Click element  css=#plone-contentmenu-factories > a
    Wait until element is visible  css=#plone-contentmenu-factories ul

The add menu item has the icon
    [Documentation]  Icon of the type in the Add menu: skin image name (Plone 4) or bootstrap icon name (Plone 6)
    [Arguments]  ${type_id}  ${icon}
    Page should contain element  css=#plone-contentmenu-factories a#${type_id} svg.bi-${icon}

The personal action links to
    [Documentation]  Item of the user menu (user actions), by action id
    [Arguments]  ${action_id}  ${url}
    Element attribute value should be  css=#personaltools-${action_id}  href  ${url}

The personal action is not available
    [Arguments]  ${action_id}
    Page should not contain element  css=#personaltools-${action_id}

The modal is open
    [Documentation]  Overlay (Plone 4) or modal (Plone 6) showing a form
    Wait until element is visible  ${MODAL} form

The modal title contains
    [Arguments]  ${text}
    Element should contain  ${MODAL} .modal-title  ${text}

Modal element
    [Documentation]  Locator of the element with this id inside the modal
    ...              (an argument starting with # would be a robot comment)
    [Arguments]  ${id}
    [Return]  ${MODAL} [id="${id}"]

Save the modal
    Click button  css=.modal-footer #form-buttons-save

Cancel the modal
    Click button  css=.modal-footer #form-buttons-cancel

The modal is closed
    Wait until page does not contain element  ${MODAL}

Select in the contact autocomplete
    [Documentation]  collective.contact.widget autocomplete: the result is chosen by its token
    [Arguments]  ${field}  ${search}  ${token}  ${title}
    Input text  css=#form-widgets-${field}-widgets-query  ${search}
    Wait until element is visible  css=li.search-result[data-token="${token}"]
    Click element  css=li.search-result[data-token="${token}"]
    Wait until page contains element  css=#formfield-form-widgets-${field} input[type=checkbox][value="${token}"]

Install the add-on
    [Arguments]  ${product}
    Go to  ${ADDONS_URL}
    Click button  xpath=//input[@name="install_product"][@value="${product}"]/following-sibling::button
    The page is not an error

Uninstall the add-on
    [Arguments]  ${product}
    Go to  ${ADDONS_URL}
    Click button  xpath=//input[@name="uninstall_product"][@value="${product}"]/following-sibling::button
    The page is not an error

The status message contains
    [Arguments]  ${text}
    Wait until element contains  css=.portalMessage  ${text}

The page is not an error
    Page should not contain  ${ERROR_PAGE_TEXT}

The page is not found
    Page should contain  ${NOT_FOUND_TEXT}

The edit link is not available
    Page should not contain element  css=#contentview-edit

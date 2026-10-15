*** Settings ***
Documentation  Plone 4.3 keywords. Same keyword names and arguments as ui_plone6.robot.
...            Robot Framework 3.x syntax (Python 2 environment).
...            Checked on Plone 4.3.20 (collective.contact.contactlist master).
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${MODAL}  css=div.overlay-ajax
${ERROR_PAGE_TEXT}  there seems to be an error
${NOT_FOUND_TEXT}  This page does not seem to exist
${ADDONS_URL}  ${PLONE_URL}/prefs_install_products_form
# icon of the contact_list type: skin image of collective.contact.core
${CONTACT_LIST_ICON}  directory_icon.png


*** Keywords ***
Log in with the login form
    [Documentation]  Real login (creates the user folder), unlike autologin
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login_form
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    Click button  css=input[name="submit"]
    # #portal-personaltools is also rendered for anonymous users
    Wait until page contains element  css=#personaltools-logout

The user is logged in
    Page should contain element  css=#personaltools-logout

Click the content action
    [Documentation]  Item of the Actions menu (object_buttons), by action id
    [Arguments]  ${action_id}
    Click element  css=#plone-contentmenu-actions dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-actions-${action_id}
    Click element  css=#plone-contentmenu-actions-${action_id}

The content action is available
    [Arguments]  ${action_id}  ${expected}=${True}
    Click element  css=#plone-contentmenu-actions dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-actions dd.actionMenuContent
    Run keyword if  ${expected}
    ...  Page should contain element  css=#plone-contentmenu-actions-${action_id}
    ...  ELSE  Page should not contain element  css=#plone-contentmenu-actions-${action_id}

Open the add menu
    Click element  css=#plone-contentmenu-factories dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-factories dd.actionMenuContent

The add menu item has the icon
    [Documentation]  Icon of the type in the Add menu: skin image name (Plone 4) or bootstrap icon name (Plone 6)
    [Arguments]  ${type_id}  ${icon}
    Page should contain element  css=#plone-contentmenu-factories a#${type_id} img[src$="/${icon}"]

The personal action links to
    [Documentation]  Item of the user menu (user actions), by action id
    [Arguments]  ${action_id}  ${url}
    Element attribute value should be  css=#personaltools-${action_id} a  href  ${url}

The personal action is not available
    [Arguments]  ${action_id}
    Page should not contain element  css=#personaltools-${action_id}

The modal is open
    [Documentation]  Overlay (Plone 4) or modal (Plone 6) showing a form
    Wait until element is visible  ${MODAL} form
    # the overlay effect and the masterselect toggles are jQuery animations
    Wait for condition  return jQuery(':animated').length == 0

The modal title contains
    [Arguments]  ${text}
    Element should contain  ${MODAL} h1.documentFirstHeading  ${text}

Modal element
    [Documentation]  Locator of the element with this id inside the modal
    ...              (an argument starting with # would be a robot comment)
    [Arguments]  ${id}
    [Return]  ${MODAL} [id="${id}"]

Save the modal
    Click button  ${MODAL} #form-buttons-save

Cancel the modal
    Click button  ${MODAL} #form-buttons-cancel

The modal is closed
    Wait until element is not visible  ${MODAL}

Select in the contact autocomplete
    [Documentation]  collective.contact.widget autocomplete (jquery.autocomplete on Plone 4):
    ...              the result is chosen by its title
    [Arguments]  ${field}  ${search}  ${token}  ${title}
    Input text  css=#form-widgets-${field}-widgets-query  ${search}
    ${result}=  Set variable  xpath=//div[contains(@class, "ac_results")]//li[contains(., "${title}")]
    Wait until element is visible  ${result}
    Click element  ${result}
    Wait until page contains element  css=#formfield-form-widgets-${field} input[type=checkbox][value="${token}"]

Install the add-on
    [Documentation]  "Activate" form of portal_quickinstaller
    [Arguments]  ${product}
    Go to  ${ADDONS_URL}
    Select checkbox  css=form[action$="/installProducts"] input[value="${product}"]
    Click button  css=form[action$="/installProducts"] input[type=submit]
    The page is not an error

Uninstall the add-on
    [Documentation]  "Deactivate" form of portal_quickinstaller
    [Arguments]  ${product}
    Go to  ${ADDONS_URL}
    Select checkbox  css=form[action$="/portal_quickinstaller"] input[value="${product}"]
    Click button  css=input[name="uninstallProducts:method"]
    The page is not an error

The status message contains
    [Arguments]  ${text}
    # the first .portalMessage of Plone 4 is the hidden #kssPortalMessage template
    Wait until element contains  css=.portalMessage:not(#kssPortalMessage)  ${text}

The page is not an error
    Page should not contain  ${ERROR_PAGE_TEXT}

The page is not found
    Page should contain  ${NOT_FOUND_TEXT}

The edit link is not available
    Page should not contain element  css=#contentview-edit

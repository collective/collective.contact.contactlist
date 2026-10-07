*** Settings ***
Documentation  Install and uninstall from the Add-ons control panel.
Resource  contactlist.robot
Test Setup  Run keywords  Open test browser  AND  Log in as manager testuser
Test Teardown  Close all browsers


*** Variables ***
${ADDONS_URL}  ${PLONE_URL}/prefs_install_products_form
${PRODUCT}  collective.contact.contactlist
${ERROR_PAGE}  there seems to be an error


*** Keywords ***
Click the add-on button
    [Arguments]  ${action}
    Go to  ${ADDONS_URL}
    Click button  xpath=//input[@name="${action}_product"][@value="${PRODUCT}"]/following-sibling::button
    Page should not contain  ${ERROR_PAGE}

The "Add to list" action is available
    [Arguments]  ${expected}=${True}
    Go to  ${ARMY_URL}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions-delete
    IF  ${expected}
        Page should contain element  css=#plone-contentmenu-actions-contactlist-addtolist
    ELSE
        Page should not contain element  css=#plone-contentmenu-actions-contactlist-addtolist
    END


*** Test Cases ***
Uninstall and reinstall the add-on
    The "Add to list" action is available
    Click the add-on button  uninstall
    The "Add to list" action is available  ${False}
    Page should not contain element  css=#personaltools-contact-contactlist-mylists
    Click the add-on button  install
    The "Add to list" action is available
    Page should contain element  css=#personaltools-contact-contactlist-mylists

A site without Members folder
    [Documentation]  as a site created without the example content
    Delete content  /plone/Members
    Go to  ${ADDONS_URL}
    Page should not contain  ${ERROR_PAGE}
    Go to  ${ARMY_URL}
    Page should not contain  ${ERROR_PAGE}
    Page should not contain element  css=#personaltools-contact-contactlist-mylists
    # reinstalling creates the Members folder
    Click the add-on button  uninstall
    Click the add-on button  install
    Go to  ${PLONE_URL}/Members
    Page should not contain  This page does not seem to exist

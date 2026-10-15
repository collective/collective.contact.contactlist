*** Settings ***
Documentation  Install and uninstall from the Add-ons control panel.
Resource  contactlist.robot
Test Setup  Run keywords  Open test browser  AND  Log in as manager testuser
Test Teardown  Close all browsers


*** Variables ***
${PRODUCT}  collective.contact.contactlist


*** Keywords ***
The "Add to list" action is available
    [Arguments]  ${expected}=${True}
    Go to  ${ARMY_URL}
    The content action is available  contactlist-addtolist  ${expected}


*** Test Cases ***
Uninstall and reinstall the add-on
    The "Add to list" action is available
    Uninstall the add-on  ${PRODUCT}
    The "Add to list" action is available  ${False}
    The personal action is not available  contact-contactlist-mylists
    Install the add-on  ${PRODUCT}
    The "Add to list" action is available
    The personal action links to  contact-contactlist-mylists  ${PLONE_URL}/Members/testuser

A site without Members folder
    [Documentation]  as a site created without the example content
    Delete content  /plone/Members
    Go to  ${ADDONS_URL}
    The page is not an error
    Go to  ${ARMY_URL}
    The page is not an error
    The personal action is not available  contact-contactlist-mylists

Reinstalling creates the Members folder
    [Documentation]  Plone 6 creates it only with the example content
    # plone6-only: Plone 4 creates the Members folder with the site, not the add-on (not run on Plone 4)
    [Tags]  plone6-only
    Delete content  /plone/Members
    Uninstall the add-on  ${PRODUCT}
    Install the add-on  ${PRODUCT}
    Go to  ${PLONE_URL}/Members
    Page should not contain  ${NOT_FOUND_TEXT}

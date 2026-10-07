*** Settings ***
Documentation  Excel export of a list (collective.excelexport): in Plone 4, a link with
...            an xls icon above the content of the list.
Resource  contactlist.robot
Test Setup  Run keywords  Open test browser  AND  Log in as manager testuser
Test Teardown  Close all browsers


*** Variables ***
${LIST_URL}  ${PLONE_URL}/Members/testuser/exported-list
${EXPORT_LINK}  xpath=//a[contains(., "Excel export list of contacts")]


*** Test Cases ***
The list has an Excel export link
    Add the contact to a new list  ${ARMY_URL}/corpsa  Exported list
    Go to  ${LIST_URL}
    Element attribute value should be  ${EXPORT_LINK}  href  ${LIST_URL}/@@collective.excelexport
    # the icon is not a broken image
    ${width}=  Execute javascript
    ...  return document.evaluate('//a[contains(., "Excel export list of contacts")]/img', document).iterateNext().naturalWidth
    Should be true  ${width} > 0

Export the list
    Add the contact to a new list  ${ARMY_URL}/corpsa  Exported list
    Go to  ${LIST_URL}
    ${response}=  Execute async javascript
    ...  var done = arguments[arguments.length - 1];
    ...  fetch('${LIST_URL}/@@collective.excelexport').then(r => done(r.status + ' ' + r.headers.get('content-type'))).catch(e => done(String(e)));
    Should match regexp  ${response}  ^200 .*excel

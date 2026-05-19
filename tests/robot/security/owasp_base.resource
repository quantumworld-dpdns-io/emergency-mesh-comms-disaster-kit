*** Settings ***
Resource    ../common.resource

*** Keywords ***
Admin Token
    ${token}=    Get Admin Token
    [Return]    ${token}

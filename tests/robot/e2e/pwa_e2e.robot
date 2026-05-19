*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Smoke
    Create Session    api    ${API_BASE}
    ${resp}=    GET On Session    api    /healthz
    Should Be Equal As Integers    ${resp.status_code}    200

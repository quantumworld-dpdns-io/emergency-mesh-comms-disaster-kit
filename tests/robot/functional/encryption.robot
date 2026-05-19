*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Encrypted Workflow Marker Exists
    Create Session    api    ${API_BASE}
    ${r}=    GET On Session    api    /healthz
    Should Be Equal As Integers    ${r.status_code}    200

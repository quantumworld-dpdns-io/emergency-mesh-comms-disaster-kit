*** Settings ***
Resource    ../common.resource

*** Test Cases ***
LoRa Path Basic API Signal
    Create Session    api    ${API_BASE}
    ${r}=    GET On Session    api    /api/v1/status
    Should Be Equal As Integers    ${r.status_code}    401

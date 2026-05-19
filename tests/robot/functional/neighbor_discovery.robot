*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Neighbor Listing Returns Data
    Create Session    api    ${API_BASE}
    ${tok}=    POST On Session    api    /api/v1/auth/token?node_id=r1&admin=false
    ${t}=    Set Variable    ${tok.json()}[token]
    ${r}=    GET On Session    api    /api/v1/neighbors    headers=${{'Authorization': 'Bearer ' + $t}}
    Should Be Equal As Integers    ${r.status_code}    200

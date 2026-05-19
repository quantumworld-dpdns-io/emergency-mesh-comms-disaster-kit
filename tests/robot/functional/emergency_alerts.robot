*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Emergency Broadcast Works
    Create Session    api    ${API_BASE}
    ${tok}=    POST On Session    api    /api/v1/auth/token?node_id=adm&admin=true
    ${t}=    Set Variable    ${tok.json()}[token]
    ${r}=    POST On Session    api    /api/v1/emergency?message=EVAC    headers=${{'Authorization': 'Bearer ' + $t}}
    Should Be Equal As Integers    ${r.status_code}    200

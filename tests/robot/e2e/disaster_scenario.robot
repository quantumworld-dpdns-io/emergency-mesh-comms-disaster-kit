*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Disaster Scenario Minimal Flow
    Create Session    api    ${API_BASE}
    ${tok}=    POST On Session    api    /api/v1/auth/token?node_id=adm&admin=true
    ${t}=    Set Variable    ${tok.json()}[token]
    ${e}=    POST On Session    api    /api/v1/emergency?message=E2E    headers=${{'Authorization': 'Bearer ' + $t}}
    Should Be Equal As Integers    ${e.status_code}    200

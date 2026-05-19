*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
Audit Endpoint Available To Admin
    Create Session    api    ${API_BASE}
    ${tokresp}=    POST On Session    api    /api/v1/auth/token?node_id=admin&admin=true
    ${token}=    Set Variable    ${tokresp.json()}[token]
    ${r}=    GET On Session    api    /api/v1/audit/events    headers=${{'Authorization': 'Bearer ' + $token}}
    Should Be Equal As Integers    ${r.status_code}    200

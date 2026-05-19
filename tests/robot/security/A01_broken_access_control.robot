*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
Admin Endpoint Denies Non Admin
    Create Session    api    ${API_BASE}
    ${resp}=    POST On Session    api    /api/v1/auth/token?node_id=u1&admin=false
    ${token}=    Set Variable    ${resp.json()}[token]
    ${r}=    POST On Session    api    /api/v1/emergency?message=x    headers=${{'Authorization': 'Bearer ' + $token}}    expected_status=403
    Should Be Equal As Integers    ${r.status_code}    403

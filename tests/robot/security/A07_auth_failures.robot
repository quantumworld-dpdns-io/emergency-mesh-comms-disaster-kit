*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
Missing Bearer Token Denied
    Create Session    api    ${API_BASE}
    ${r}=    GET On Session    api    /api/v1/status    expected_status=401
    Should Be Equal As Integers    ${r.status_code}    401

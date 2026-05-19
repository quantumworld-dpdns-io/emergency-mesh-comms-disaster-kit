*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
Null Byte Injection Rejected
    Create Session    api    ${API_BASE}
    ${resp}=    POST On Session    api    /api/v1/auth/token?node_id=u1&admin=false
    ${token}=    Set Variable    ${resp.json()}[token]
    ${headers}=    Create Dictionary    Authorization=Bearer ${token}
    ${r}=    POST On Session    api    /api/v1/bundles    headers=${headers}    data={"destination_eid":"dtn://x","payload":"a\u0000b","priority":"general"}    expected_status=400
    Should Be Equal As Integers    ${r.status_code}    400

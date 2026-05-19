*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
Large Payload Rejected
    Create Session    api    ${API_BASE}
    ${resp}=    POST On Session    api    /api/v1/auth/token?node_id=u1&admin=false
    ${token}=    Set Variable    ${resp.json()}[token]
    ${big}=    Evaluate    "x" * (1024*1024+10)
    ${headers}=    Create Dictionary    Authorization=Bearer ${token}
    ${r}=    POST On Session    api    /api/v1/bundles    headers=${headers}    json=${{'destination_eid':'dtn://x','payload':$big,'priority':'general'}}    expected_status=413
    Should Be Equal As Integers    ${r.status_code}    413

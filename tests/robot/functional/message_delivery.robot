*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Message Delivery Queue Path
    Create Session    api    ${API_BASE}
    ${tok}=    POST On Session    api    /api/v1/auth/token?node_id=r1&admin=false
    ${t}=    Set Variable    ${tok.json()}[token]
    ${r}=    POST On Session    api    /api/v1/messages    headers=${{'Authorization': 'Bearer ' + $t, 'X-API-Key': 'dev-api-key'}}    json=${{'to_eid':'dtn://node-2','text':'rf-msg','priority':'general'}}
    Should Be Equal As Integers    ${r.status_code}    200

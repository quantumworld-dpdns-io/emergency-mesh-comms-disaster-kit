*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Bundle Submission Queues
    Create Session    api    ${API_BASE}
    ${tok}=    POST On Session    api    /api/v1/auth/token?node_id=r1&admin=false
    ${t}=    Set Variable    ${tok.json()}[token]
    ${r}=    POST On Session    api    /api/v1/bundles    headers=${{'Authorization': 'Bearer ' + $t}}    json=${{'destination_eid':'dtn://node-2','payload':'sf','priority':'general'}}
    Should Be Equal As Integers    ${r.status_code}    200

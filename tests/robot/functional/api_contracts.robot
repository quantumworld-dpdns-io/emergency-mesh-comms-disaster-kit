*** Settings ***
Resource    ../common.resource

*** Test Cases ***
OpenAPI Surface Behaviors
    Create Session    api    ${API_BASE}
    ${r1}=    GET On Session    api    /api/v1/status    expected_status=401
    ${r2}=    GET On Session    api    /healthz
    Should Be Equal As Integers    ${r2.status_code}    200

*** Settings ***
Resource    ../common.resource

*** Test Cases ***
Node Startup API Ready
    Create Session    api    ${API_BASE}
    ${health}=    GET On Session    api    /healthz
    ${ready}=    GET On Session    api    /readyz
    Should Be Equal As Integers    ${health.status_code}    200
    Should Be Equal As Integers    ${ready.status_code}    200

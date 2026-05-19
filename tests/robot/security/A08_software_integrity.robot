*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
Wasm Signature Verification Endpoint Placeholder
    Create Session    api    ${API_BASE}
    ${r}=    GET On Session    api    /healthz
    Should Be Equal As Integers    ${r.status_code}    200

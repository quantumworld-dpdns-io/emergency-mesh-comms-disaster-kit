*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
Security Headers Present
    Create Session    api    ${API_BASE}
    ${r}=    GET On Session    api    /healthz
    Dictionary Should Contain Key    ${r.headers}    X-Content-Type-Options
    Dictionary Should Contain Key    ${r.headers}    Content-Security-Policy

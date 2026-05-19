*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
No Secrets In Health Response
    Create Session    api    ${API_BASE}
    ${r}=    GET On Session    api    /healthz
    Should Be Equal As Integers    ${r.status_code}    200
    Should Not Contain    ${r.text}    SECRET_KEY

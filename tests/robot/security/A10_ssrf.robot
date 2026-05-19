*** Settings ***
Resource    owasp_base.resource

*** Test Cases ***
No Arbitrary URL Fetch Endpoint
    Create Session    api    ${API_BASE}
    ${r}=    GET On Session    api    /api/v1/fetch?url=http://169.254.169.254    expected_status=404
    Should Be Equal As Integers    ${r.status_code}    404

*** Settings ***
Library    RequestsLibrary

*** Variables ***
${API_BASE}    http://localhost:8080

*** Keywords ***
Get Admin Token
    Create Session    api    ${API_BASE}
    ${resp}=    POST On Session    api    /api/v1/auth/token?node_id=robot&admin=true
    ${body}=    Set Variable    ${resp.json()}
    [Return]    ${body}[token]

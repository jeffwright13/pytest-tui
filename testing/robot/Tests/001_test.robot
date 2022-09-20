*** Settings ***
Resource    ../Resources/common.resource
Library     Process

*** Test Cases ***
Get Python Version
    ${result} =         Run Process         python          --version
    Should Contain      ${result.stdout}    Python 3.10.5

Get Pytest Version
    ${result} =         Run Process         pytest          --version
    Should Contain      ${result.stdout}    pytest 7.2.0.dev264+g6ad32a9c5

Verify Pytest-Tui Option in Pytest Help
    ${result} =         Run Process         pytest          --help
    Should Contain      ${result.stdout}    tui:
    Should Contain      ${result.stdout}    --tui
    Should Contain      ${result.stdout}    Enable the pytest-tui plugin.

Get Pytest-Tui Version
    ${result} =         Run Process         pytest          -VV
    Should Contain      ${result.stdout}    pytest-tui-1.4.1

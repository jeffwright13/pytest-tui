*** Settings ***
Resource    ../Resources/common.resource
Library     Process
Library     SeleniumLibrary

*** Test Cases ***
Verify Script Launch: 'tuih'
    ${result} =         Run Process     python %{TOX_ROOT}/pytest_tui/html_gen.py   timeout=1min
    Should Be Equal As Integers         ${result.rc}	0

*** Variables ***


*** Comments ***

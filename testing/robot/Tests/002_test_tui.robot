*** Settings ***
Resource    ../Resources/common.resource
Library     Process
Library     SeleniumLibrary

*** Test Cases ***
Verify Basic Test Run
    ${result} =         Run Process         pytest          --tui      -k   test_0
    Should Contain      ${result.stdout}    == short test summary info ==

Verify Script Launch: 'tui'
    ${result} =         Run Process         tui         timeout=10sec
    Log To Console      ${result.stdout}
    Should Contain      ${result.stdout}    ${HEADER}   timeout=10

Quit TUI
    Press Keys          None    q


*** Variables ***
${HEADER} =    │ Summary │ Passes │ Failures │ Skipped │ Xfails │ Xpasses │ Warnings │ Errors │ Full Output │ Quit (Q) │


*** Comments ***

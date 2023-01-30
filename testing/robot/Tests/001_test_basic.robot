*** Settings ***
Resource    ../Resources/common.resource
Library     Process

*** Test Cases ***
Print Environment Variables
    Log To Console    %{PYTHON_VERSION}
    Log To Console    %{PYTEST_TUI_VERSION}

Verify Python Version
    ${result} =         Run Process         python          --version
    Should Contain      ${result.stdout}    %{PYTHON_VERSION}

Verify Pytest-Tui Option Shows in Pytest Help
    ${result} =         Run Process         pytest          --help
    Should Contain      ${result.stdout}    tui:
    Should Contain      ${result.stdout}    --tui
    Should Contain      ${result.stdout}    Enable the pytest-tui plugin.

Verify Pytest-Tui Version
    ${result} =         Run Process         pytest          -VV         --co
    Should Contain      ${result.stdout}    %{PYTEST_TUI_VERSION}

Verify Basic Test Run
    ${result} =         Run Process         pytest          --tui      -k   test_0
    Log To Console      ${result.stdout}
    Should Contain      ${result.stdout}    short test summary info

*** Comments ***
Verify Full Test Run
    ${result} =         Run Process         pytest          --tui
    # Log To Console      ${result.stdout}
    Should Contain      ${result.stdout}    short test summary info

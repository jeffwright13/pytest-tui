#!/bin/bash

clean_up() {
  test -d "$1" && rm -rf "$1"
}

printf "%s\n" "$0"
printf "%s\n" "$1"

tmpdir=$( mktemp -d -t pytest-tui )
printf "Creating temporary directory %s\n" "$tmpdir"
cd "$tmpdir" || exit

printf "Creating virtual Python environment with Python version %s\n" "$1"
pyenv local "$1"
python --version

# Verify Python version being used is one being tested
[[ $1 == $(python --version | awk '{print $2}') ]] || { echo "Python version being used is not the one being tested - are you running this script from a virtual environment? Exiting..."; exit 1; }

python -m venv venv
source ./venv/bin/activate

printf "Upgrading build tools\n"
pip install --upgrade pip setuptools wheel

printf "Installing pytest-tui from Test-PyPi\n"
pip install -i https://test.pypi.org/simple/ pytest-tui
pip install pytest-rerunfailures

printf "\Cloning pytest-tui so we can use its demo-tests\n"
git clone git@github.com:jeffwright13/pytest-tui.git
mkdir demo-tests
cp pytest-tui/demo-tests/* ./demo-tests/
clean_up pytest-tui
ls -la demo-tests/
rm -f conftest.py

printf "Executing pytest-tui\n"
pytest --tui -k test_0

printf "Launching TUI and verifying content\n"
expect <(cat <<'EOD'
  spawn tui
  # interact
  expect {"Summary"}
  # expect {"Passes"}
  # expect {"Failures"}
  # expect {"Skipped"}
  # expect {"Xfails"}
  # expect {"Xpasses"}
  # expect {"Warnings"}
  # expect {"Errors"}
  # expect {"Full Output"}
  # expect {"Quit (Q)"}    sleep 5
    send "q"
    exit
EOD
)



# Recover from any ANSI corruption that may have occured as a result of running pytest-tui
reset

printf "Launching HTML\n"
tuih

clean_up "$tmpdir"
printf "Script finished"

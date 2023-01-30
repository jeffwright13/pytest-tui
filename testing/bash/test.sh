#!/bin/bash

set -eu

function usage() {
  printf "\nUsage: test.sh [--version PYTHON_VERSION] [--help]\n"
  exit 1
}

clean_up() {
  test -d "$1" && rm -rf "$1"
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --version) shift; pyversion="$1" ;;
    --help) usage ;;
    --) shift; break ;;
    -*) echo "Unknown flag '$1'" 1>&2; usage ;;
    *) break ;;
  esac
  shift
done

printf "%s %s\n" "$0" "$pyversion"

tmpdir=$( mktemp -d -t pytest-tui )
printf "Creating temporary directory %s\n" "$tmpdir"
cd "$tmpdir" || exit

# Use Python version specified on command line
printf "Creating virtual Python environment with Python version %s\n" "$pyversion"
pyenv local "$pyversion"

# Verify Python version being used is one being tested
[[ $pyversion == $(python --version | awk '{print $2}') ]] || { echo "Python version being used is not the one being tested - are you running this script from a virtual environment? Exiting..."; exit 1; }

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

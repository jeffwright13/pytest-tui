#!/bin/bash

clean_up() {
  test -d "$tmpdir" && rm -ri "$tmpdir"
}

tmpdir=$( mktemp -d -t pytest-tui )
printf "Creating temporary directory %s" "$tmpdir"

cd "$tmpdir" || exit

printf "\nCreating virtual Python environment"
pyenv local 3.11.1
python -m venv venv
source ./venv/bin/activate

printf "\nUpgrading build tools"
pip install --upgrade pip setuptools wheel

printf "\nInstalling pytest-tui"
pip install pytest-tui
pip list | grep pytest-tui

printf "\nInstalling pytest-tui"
git clone git@github.com:jeffwright13/pytest-tui.git
ls -la
rm -f conftest.py

printf "\nExecuting pytest-tui"
cd pytest-tui || exit
pytest --tui

tui
q
tuih

trap 'clean_up $tmpdir' EXIT

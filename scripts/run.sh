#!/bin/bash

venv_dir=.venv
bin="$venv_dir/bin"

python -m venv "$venv_dir"
"$bin/pip" install -r requirements.txt
"$bin/flask" db upgrade
"$bin/flask" run

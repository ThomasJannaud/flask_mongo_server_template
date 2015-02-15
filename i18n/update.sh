#!/bin/bash

BABEL_EXE=/usr/local/bin/pybabel
$BABEL_EXE extract -F babel.cfg -o messages.pot ..
# first time running this : run init line, not update
#$BABEL_EXE init -i messages.pot -d translations -l fr
$BABEL_EXE update -i messages.pot -d translations
$BABEL_EXE compile -f -d translations

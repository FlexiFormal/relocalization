#!/bin/sh

rustex_exe="${1}"
export MATHHUB="${MATHHUB},../.."
"${rustex_exe}" -i odd-even-example-1.en.tex -o odd-even-example-1.en.html

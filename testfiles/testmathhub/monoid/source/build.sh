#!/bin/sh

rustex_exe="${1}"
"${rustex_exe}" -i commutative-monoid.en.tex -o commutative-monoid.en.html
"${rustex_exe}" -i invertible-in-monoid.en.tex -o invertible-in-monoid.en.html

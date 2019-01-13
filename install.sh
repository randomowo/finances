#!/bin/bash

cp src/main.py /usr/local/bin/fin
if [[ -f "/usr/local/bin/fin" ]]; then chmod 766 /usr/local/bin/fin; fi

echo "Thank you for installation!\n To use use (tput setaf 1) fin"
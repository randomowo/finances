#!/bin/bash

if [[ -f "usr/local/bin/fin" ]] && [[ -f "/tmp/finances.pkl" ]]; then
    rm /usr/local/bin/fin
    rm /tmp/finances.pkl
fi